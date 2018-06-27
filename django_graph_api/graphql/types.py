from collections import (
    OrderedDict,
    Iterable
)
from inspect import isclass
import copy

from django.db.models import Manager
from django.utils import six

from django_graph_api.graphql.utils import (
    GraphQLError
)
from django_graph_api.graphql.ast_helpers import (
    get_input_value,
    get_selections
)

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

    def __init__(self, description=None, arguments=None, null=True):
        self.arguments = arguments or {}
        self.description = description
        self.null = null

        # Increase the creation counter, and save our local copy.
        self.creation_counter = Field.creation_counter
        Field.creation_counter += 1
        # This is so that a field can be introspected to see if it
        # has been bound.
        self._bound = False
        self.errors = []

    def get_value(self):
        raw_value = self.get_raw_value()
        if not self.null and raw_value is None:
            raise GraphQLError('Field {} returned null but is not nullable'.format(self.name))
        if hasattr(self.type_, 'coerce_result'):
            try:
                return self.type_.coerce_result(raw_value)
            except ValueError:
                raise GraphQLError('Cannot coerce {} ({}) to {}'.format(
                    type(raw_value).__name__,
                    raw_value,
                    self.type_.object_name
                ))
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
        if not self._bound:
            raise GraphQLError('Usage exception: must bind Field to a selection and object first')

        resolver_args = {name: None for name in self.arguments}

        for name, value in self.selection_arguments.items():
            arg_type = self.arguments.get(name)
            if not arg_type:
                continue
            try:
                arg_value = arg_type.coerce_input(value)
                resolver_args[name] = arg_value
            except ValueError:
                error = 'Query error: Argument {} expected a {} but got a {}'.format(
                    name,
                    type(arg_type),
                    type(value)
                )
                raise GraphQLError(error)
        return resolver_args

    def bind(self, selection, obj):
        self.selection = selection
        self.name = selection.name
        self.obj = obj
        self._bound = True
        self.selection_arguments = {
            arg.name: get_input_value(arg.value, obj.variables, obj.variable_definitions)
            for arg in self.selection.arguments
        }


class Scalar(six.with_metaclass(ObjectNameMetaclass)):
    kind = SCALAR

    def __init__(self, null=True):
        self.null = null

    def __eq__(self, other):
        if self.__class__ == other.__class__:
            return True
        return False

    @property
    def name(self):
        return self.object_name


class MockScalar(Scalar):
    @classmethod
    def coerce_result(cls, value):
        return None


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
        if isinstance(value, bool):
            return value
        raise ValueError(
            "Could not coerce {} of type {} to boolean. Must be true or false".format(value, type(value).__name__)
        )


class Enum(Scalar):
    kind = ENUM
    values = ()


class NonNull(object):
    kind = NON_NULL
    null = True

    def __init__(self, type_):
        self.type_ = type_

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.type_ == other.type_


class List(object):
    kind = LIST

    def __init__(self, type_, null=True):
        self.type_ = type_
        self.null = null

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
        # implementation. We also allow explicit introspection_fields
        # declaration in order to get around python's munging of double
        # underscores.
        declared_fields = OrderedDict()

        if 'introspection_fields' in attrs:
            declared_fields.update(copy.deepcopy(attrs['introspection_fields']))

        parents = [b for b in bases if isinstance(b, ObjectMetaclass)]
        for parent in reversed(parents):
            declared_fields.update(copy.deepcopy(parent._declared_fields))

        for key, value in list(attrs.items()):
            if isinstance(value, Field):
                declared_fields[key] = value
                del attrs[key]
        attrs['_declared_fields'] = declared_fields

        cls = super(ObjectMetaclass, mcs).__new__(mcs, name, bases, attrs)

        for name, field in declared_fields.items():
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

    def __init__(self, ast, data, fragments, variable_definitions=None, variables=None):
        self.ast = ast
        self.data = data
        self.fragments = fragments
        self.variable_definitions = variable_definitions or {}
        self.variables = variables or {}
        self.errors = []

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
            # If the field doesn't exist, create a dummy field that returns None
            for selection in selections:
                try:
                    field = copy.deepcopy(self._declared_fields[selection.name])
                except KeyError:
                    self.errors.append(
                        GraphQLError('{} does not have field {}'.format(self.object_name, selection.name))
                    )
                    field = Field()
                    field.type_ = MockScalar

                self._fields[selection.name] = field
                field.bind(selection=selection, obj=self)
        return self._fields

    def execute(self):
        data = {}
        for name, field in self.fields.items():
            try:
                value = field.get_value()
                self.errors.extend(field.errors)
            except Exception as e:
                value = None
                self.errors.append(
                    GraphQLError('Error resolving {}: {}'.format(name, e))
                )
            data[name] = value

        return data, self.errors


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
        def _str_to_class(s):
            try:
                module_name, class_name = s.rsplit('.', 1)
                module = __import__(module_name, fromlist=(class_name,))
                class_ = getattr(module, class_name)
                return class_
            except (ValueError, AttributeError, ImportError):
                return None

        if not isclass(self._object_type):
            if callable(self._object_type):
                self._object_type = self._object_type()
            elif self._object_type == 'self':
                self._object_type = self._self_object_type
            elif isinstance(self._object_type, str):
                    object_type = _str_to_class(self._object_type)
                    if object_type is not None:
                        self._object_type = object_type
        if not isclass(self._object_type):
            raise ValueError(
                'Invalid object_type: "{}"'.format(self._object_type)
            )
        return self._object_type

    def _execute_related(self, value):
        obj_instance = self.get_object_instance(value)
        data, errors = obj_instance.execute()
        self.errors.extend(errors)
        return data

    def get_value(self):
        value = super(RelatedField, self).get_value()
        if value is None:
            return None
        return self._execute_related(value)

    def get_object_instance(self, value=None):
        return self.object_type(
            ast=self.selection,
            data=value,
            fragments=self.obj.fragments,
            variable_definitions=self.obj.variable_definitions,
            variables=self.obj.variables
        )


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
            self._execute_related(value)
            for value in values
        ]
