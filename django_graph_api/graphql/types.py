import copy

from collections import OrderedDict

from .schema import schema


SCALAR = 'SCALAR'
OBJECT = 'OBJECT'
INTERFACE = 'INTERFACE'
UNION = 'UNION'
ENUM = 'ENUM'
INPUT_OBJECT = 'INPUT_OBJECT'
LIST = 'LIST'
NON_NULL = 'NON_NULL'

schema.register_type_kind(SCALAR)
schema.register_type_kind(OBJECT)
schema.register_type_kind(INTERFACE)
schema.register_type_kind(UNION)
schema.register_type_kind(ENUM)
schema.register_type_kind(INPUT_OBJECT)
schema.register_type_kind(LIST)
schema.register_type_kind(NON_NULL)


class Field(object):
    """
    Fields are used for schema definition and result coercion.
    """
    # Tracks each time a Field instance is created. Used to retain order.
    creation_counter = 0

    def __init__(self):
        # Increase the creation counter, and save our local copy.
        self.creation_counter = Field.creation_counter
        Field.creation_counter += 1

    def get_value(self):
        return self.obj.kwargs.get(self.name)

    def bind(self, name, obj):
        self.name = name
        self.obj = obj


class Scalar(object):
    kind = SCALAR

    @property
    def name(self):
        return self.__class__.__name__


@schema.register_type
class Int(Scalar):
    def coerce_result(self, value):
        return int(value)


@schema.register_type
class Float(Scalar):
    def coerce_result(self, value):
        return float(value)


@schema.register_type
class String(Scalar):
    def coerce_result(self, value):
        return str(value)


@schema.register_type
class Id(String):
    name = 'ID'


@schema.register_type
class Boolean(Scalar):
    def coerce_result(self, value):
        return bool(value)


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


@schema.register_type
class Object(object, metaclass=ObjectMetaclass):
    kind = OBJECT

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    @property
    def fields(self):
        if not hasattr(self, '_fields'):
            self._fields = OrderedDict()
            # Copy the field instances so that obj instances have
            # isolated field instances that they can modify safely.
            declared_fields = copy.deepcopy(self._declared_fields)
            for name, field in declared_fields.items():
                self._fields[name] = field
                field.bind(name=name, obj=self)
        return self._fields

    def serialize(self):
        ret = {}

        for name, field in self.fields.items():
            value = field.get_value()
            ret[name] = value

        return ret


class CharField(Field):
    type_ = String


class IdField(CharField):
    type_ = Id


class FloatField(Field):
    type_ = Float


class IntegerField(Field):
    type_ = Int


class BooleanField(Field):
    type_ = Boolean


class ObjectField(Field):
    type_ = Object

    def __init__(self, object_type):
        self.object_type = object_type

    def get_value(self):
        get_data = getattr(self.obj, 'get_{}'.format(self.name))
        obj_instance = self.object_type(**get_data())
        return obj_instance.serialize()
