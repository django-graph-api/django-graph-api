import copy
import pdb

from collections import OrderedDict
from inspect import isclass

from django.db.models import Manager
from django.utils import six

SCALAR = 'SCALAR'
OBJECT = 'OBJECT'
INTERFACE = 'INTERFACE'
UNION = 'UNION'
ENUM = 'ENUM'
INPUT_OBJECT = 'INPUT_OBJECT'
LIST = 'LIST'
NON_NULL = 'NON_NULL'


def get_arguments_for_selection(ast, name):
    selection = next((s for s in ast.selections if s.name == name), None)
    if not selection:
        return {}

    return selection.arguments


class Field(object):
    """
    Fields are used for schema definition and result coercion.
    """
    # Tracks each time a Field instance is created. Used to retain order.
    creation_counter = 0
    _arguments = {}

    def __init__(self, **kwargs):
        self._arguments = kwargs
        # Increase the creation counter, and save our local copy.
        self.creation_counter = Field.creation_counter
        Field.creation_counter += 1

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
        arguments = {arg.name: arg.value for arg in get_arguments_for_selection(self.obj.ast, self.name)}
        resolver_kwargs = {}
        for key, value in self._arguments.items():
            if key in arguments:
                input_value = arguments[key]
                try:
                    arg_value = value.coerce_result(input_value)
                except TypeError:
                    error = 'Argument {} expected a {} but got a {}'.format(key, type(value), type(input_value))
                    raise TypeError(error)
                resolver_kwargs[key] = arg_value
            else:
                resolver_kwargs[key] = None
        return resolver_kwargs

    def bind(self, selection, obj):
        self.selection = selection
        self.name = selection.name
        self.obj = obj


class Scalar(object):
    kind = SCALAR

    @property
    def name(self):
        return self.__class__.__name__


class Int(Scalar):
    @classmethod
    def coerce_result(cls, value):
        return None if value is None else int(value)


class Float(Scalar):
    @classmethod
    def coerce_result(cls, value):
        return None if value is None else float(value)


class String(Scalar):
    @classmethod
    def coerce_result(cls, value):
        return None if value is None else str(value)


class Id(String):
    name = 'ID'


class Boolean(Scalar):
    @classmethod
    def coerce_result(cls, value):
        return None if value is None else bool(value)


class List(object):
    kind = LIST

    def __init__(self, type_):
        self.type_ = type_

    @classmethod
    def coerce_result(cls, values):
        if values is None:
            return None
        if isinstance(values, Manager):
            values = values.all()
        return list(values)


class ObjectMetaclass(type):
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

        return super(ObjectMetaclass, mcs).__new__(mcs, name, bases, attrs)


class Object(six.with_metaclass(ObjectMetaclass)):
    """
    Subclass this to define an object node in a schema.

    e.g.
    ::

        class Character(Object):
            name = CharField()
    """
    kind = OBJECT

    def __init__(self, ast, data):
        self.ast = ast
        self.data = data

    @property
    def fields(self):
        if not hasattr(self, '_fields'):
            self._fields = OrderedDict()
            # Copy the field instances so that obj instances have
            # isolated field instances that they can modify safely.
            # Only copy field instances that are selected.
            for selection in self.ast.selections:
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
        self.object_type = object_type
        super(RelatedField, self).__init__(**kwargs)

    @classmethod
    def resolve_object_type(cls, object_type):
        if callable(object_type) and not isclass(object_type):
            return object_type()
        return object_type

    def bind(self, selection, obj):
        super(RelatedField, self).bind(selection, obj)
        self.object_type = self.__class__.resolve_object_type(self.object_type)
        if self.object_type == 'self':
            self.object_type = obj.__class__

    def _serialize_value(self, value):
        obj_instance = self.object_type(
            ast=self.selection,
            data=value,
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
