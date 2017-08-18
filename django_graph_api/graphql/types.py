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


class Object(object):
    kind = OBJECT
