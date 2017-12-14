from collections import (
    OrderedDict,
    Iterable
)
from inspect import isclass
import copy

from django.db.models import Manager
from django.utils import six

from django_graph_api.graphql.utils import get_selections


SCALAR = 'SCALAR'
OBJECT = 'OBJECT'
INTERFACE = 'INTERFACE'
UNION = 'UNION'
ENUM = 'ENUM'
INPUT_OBJECT = 'INPUT_OBJECT'
LIST = 'LIST'
NON_NULL = 'NON_NULL'

TYPE_KINDS_VALUES = (
    SCALAR,
    OBJECT,
    INTERFACE,
    UNION,
    ENUM,
    INPUT_OBJECT,
    LIST,
    NON_NULL,
)


class ObjectNameMetaclass(type):
    def __new__(mcs, name, bases, attrs):
        if 'object_name' not in attrs:
            attrs['object_name'] = name

        return super(ObjectNameMetaclass, mcs).__new__(mcs, name, bases, attrs)


class Field(object):
    """
    Fields are used for schema definition and result coercion.
    """
    # Tracks each time a Field instance is created. Used to retain order.
    creation_counter = 0
    arguments = {}

    def __init__(self, **kwargs):
        self.arguments = kwargs
        # Increase the creation counter, and save our local copy.
        self.creation_counter = Field.creation_counter
        Field.creation_counter += 1
        # This is so that a field can be introspected to see if it
        # has been bound.
        self._bound = False

    def get_value(self):
        raw_value = self.get_raw_value()
        if hasattr(self.type_, 'coerce_result'):
            try:
                return self.type_.coerce_result(raw_value)
            except ValueError:
                return None
        return raw_value

    def get_raw_value(self):
        # Try user defined resolver
        if hasattr(self.obj, 'get_{}'.format(self.name)):
            kwargs = self.get_resolver_args()
            resolver = getattr(self.obj, 'get_{}'.format(self.name))
            return resolver(**kwargs)

        # Try model attributes
        data = self.obj.data
        try:
            return getattr(data, self.name)
        except AttributeError:
            pass

        try:
            return data.get(self.name)
        except (AttributeError, KeyError):
            pass

        return None

    def get_resolver_args(self):
        arguments = {arg.name: arg.value for arg in self.selection.arguments}
        resolver_args = {}
        for key, value in self.arguments.items():
            if key in arguments:
                input_value = arguments[key]
                try:
                    arg_value = value.coerce_input(input_value)
                except TypeError:
                    error = 'Argument {} expected a {} but got a {}'.format(key, type(value), type(input_value))
                    raise TypeError(error)
                resolver_args[key] = arg_value
            else:
                resolver_args[key] = None
        return resolver_args

    def bind(self, selection, obj):
        self.selection = selection
        self.name = selection.name
        self.obj = obj
        self._bound = True


class Scalar(six.with_metaclass(ObjectNameMetaclass)):
    kind = SCALAR

    def __eq__(self, other):
        if self.__class__ == other.__class__:
            return True
        return False

    @property
    def name(self):
        return self.object_name


class Int(Scalar):
    @classmethod
    def coerce_result(cls, value):
        return None if value is None else int(value)

    @classmethod
    def coerce_input(cls, value):
        if value is None:
            return None
        if not isinstance(value, int) or isinstance(value, bool):
            raise ValueError('Expected an int type, got {}'.format(type(value)))
        min_value = -2147483648  # -2**31
        max_value = 2147483647  # 2**31 - 1
        if value < min_value or value > max_value:
            raise ValueError('Value must be between {} and {} (inclusive). Got {}'.format(
                min_value, max_value, value))
        return value


class Float(Scalar):
    @classmethod
    def coerce_result(cls, value):
        return None if value is None else float(value)

    @classmethod
    def coerce_input(cls, value):
        if value is None:
            return None
        if not isinstance(value, (float, int)) or isinstance(value, bool):
            raise ValueError('Expected a float type, got {}'.format(type(value)))
        return None if value is None else float(value)


class String(Scalar):
    @classmethod
    def coerce_result(cls, value):
        return None if value is None else six.text_type(value)

    @classmethod
    def coerce_input(cls, value):
        if value is None:
            return None
        if not isinstance(value, six.string_types):
            raise ValueError('Expected a string/unicode type, got {}'.format(type(value)))
        return None if value is None else six.text_type(value)


class Id(String):
    object_name = 'ID'


class Boolean(Scalar):
    @classmethod
    def coerce_result(cls, value):
        return None if value is None else bool(value)

    @classmethod
    def coerce_input(cls, value):
        if value is None:
            return None
        if not isinstance(value, bool):
            raise ValueError('Expected a bool type, got {}'.format(type(value)))
        return value


class Enum(Scalar):
    kind = ENUM
    values = ()


class List(object):
    kind = LIST

    def __init__(self, type_):
        self.type_ = type_

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.type_ == other.type_

    def coerce_result(self, values):
        if values is None:
            return None
        if isinstance(values, Manager):
            values = values.all()
        elif isinstance(values, six.string_types):
            values = [values]
        if issubclass(self.type_, Scalar):
            return [self.type_.coerce_result(value) for value in list(values)]
        return list(values)

    def coerce_input(self, values):
        if values is None:
            return None
        if not isinstance(values, Iterable) or isinstance(values, six.string_types):
            values = [values]
        return [self.type_.coerce_input(value) for value in values]


class ObjectMetaclass(ObjectNameMetaclass):
    def __new__(mcs, name, bases, attrs):
        # This fields implementation is similar to Django's form fields
        # implementation. Currently we do not support inheritance of fields.
        current_fields = []
        for key, value in list(attrs.items()):
            if isinstance(value, Field):
                current_fields.append((key, value))
                attrs.pop(key)
        current_fields.sort(key=lambda x: x[1].creation_counter)
        attrs['_declared_fields'] = OrderedDict(current_fields)

        cls = super(ObjectMetaclass, mcs).__new__(mcs, name, bases, attrs)

        for name, field in current_fields:
            field._self_object_type = cls

        return cls


class Object(six.with_metaclass(ObjectMetaclass)):
    """
    Subclass this to define an object node in a schema.

    e.g.
    ::

        class Character(Object):
            name = CharField()
    """
    kind = OBJECT

    def __init__(self, ast, data, fragments):
        self.ast = ast
        self.data = data
        self.fragments = fragments

    @property
    def fields(self):
        if not hasattr(self, '_fields'):
            self._fields = OrderedDict()

            selections = get_selections(
                selections=self.ast.selections,
                fragments=self.fragments,
                object_type=self.__class__,
            )

            # Copy the field instances so that obj instances have
            # isolated field instances that they can modify safely.
            # Only copy field instances that are selected.
            for selection in selections:
                field = copy.deepcopy(self._declared_fields[selection.name])
                self._fields[selection.name] = field
                field.bind(selection=selection, obj=self)
        return self._fields

    def serialize(self):
        return {
            name: field.get_value()
            for name, field in self.fields.items()
        }


class CharField(Field):
    """
    Defines a string field.

    Querying on this field will return a str or None.
    """
    type_ = String


class IdField(CharField):
    """
    Defines an id field.

    Querying on this field will return a str or None.
    """

    type_ = Id


class FloatField(Field):
    """
    Defines a float field.

    Querying on this field will return a float or None.
    """
    type_ = Float


class IntegerField(Field):
    """
    Defines an integer field.

    Querying on this field will return an int or None.
    """
    type_ = Int


class BooleanField(Field):
    """
    Defines a boolean field.

    Querying on this field will return a bool or None.
    """
    type_ = Boolean


class EnumField(CharField):
    type_ = Enum

    def __init__(self, enum):
        super(EnumField, self).__init__()

        self.enum = enum


class ManyEnumField(EnumField):
    type_ = List(String)


class RelatedField(Field):
    """
    Defines a many-to-1 or 1-to-1 related field.

    e.g.
    ::

        class Character(Object):
            name = CharField()
            mother = RelatedField('self')

    Can be queried like
    ::

        ...
        character {
            mother {
                name
            }
        }
        ...

    And would return
    ::

        ...
        "character": {
            "mother": {
                "name": "Joyce Summers"
            }
        }
        ...
    """
    type_ = Object

    def __init__(self, object_type, **kwargs):
        self._object_type = object_type
        super(RelatedField, self).__init__(**kwargs)

    @property
    def object_type(self):
        if not isclass(self._object_type):
            if callable(self._object_type):
                self._object_type = self._object_type()
            if self._object_type == 'self':
                self._object_type = self._self_object_type
        return self._object_type

    def _serialize_value(self, value):
        obj_instance = self.object_type(
            ast=self.selection,
            data=value,
            fragments=self.obj.fragments,
        )
        return obj_instance.serialize()

    def get_value(self):
        value = super(RelatedField, self).get_value()
        if value is None:
            return None
        return self._serialize_value(value)


class ManyRelatedField(RelatedField):
    """
    Defines a 1-to-many or many-to-many related field.

    e.g.
    ::

        class Character(Object):
            name = CharField()
            friends = RelatedField('self')

    Can be queried like
    ::

        ...
        character {
            friends {
                name
            }
        }
        ...

    And would return
    ::

        ...
        "character": {
            "friends": [
                {"name": "Luke Skywalker"},
                {"name": "Han Solo"}
            ]
        }
        ...
    """
    type_ = List(Object)

    def get_value(self):
        values = super(RelatedField, self).get_value()
        if values is None:
            return None
        if isinstance(values, Manager):
            values = values.all()
        return [
            self._serialize_value(value)
            for value in values
        ]
