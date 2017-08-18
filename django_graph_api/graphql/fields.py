from .types import (
    Float,
    Int,
    String,
    Id,
    Boolean,
)


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

    def get_value(self, arguments=None, fields=None):
        raise NotImplementedError

    def bind(self, name, node):
        self.name = name
        self.node = node


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
