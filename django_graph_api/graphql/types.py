from collections import OrderedDict
import copy

from django.db.models import Manager

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

    def get_value(self, ast):
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


@schema.register_type
class List(object):
    kind = LIST

    def __init__(self, type_):
        self.type_ = type_

    def coerce_result(self, values):
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


@schema.register_type
class Object(object, metaclass=ObjectMetaclass):
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
            declared_fields = copy.deepcopy(self._declared_fields)
            for name, field in declared_fields.items():
                self._fields[name] = field
                field.bind(name=name, obj=self)
        return self._fields

    def serialize(self):
        return {
            name: field.get_value(self.ast)
            for name, field in self.fields.items()
        }


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


class RelatedField(Field):
    type_ = Object

    def __init__(self, object_type):
        self.object_type = object_type

    def _serialize_value(self, value, ast):
        obj_instance = self.object_type(
            ast=ast,
            data=value,
        )
        return obj_instance.serialize()

    def get_value(self, ast):
        value = super(RelatedField, self).get_value(ast)
        return self._serialize_value(value, ast)


class ManyRelatedField(Field):
    type_ = List(Object)

    def __init__(self, object_type):
        self.object_type = object_type

    def get_value(self, ast):
        values = super(RelatedField, self).get_value(ast)
        if isinstance(values, Manager):
            values = values.all()
        return [
            self._serialize_value(value, ast)
            for value in values
        ]
