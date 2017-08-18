import copy

from collections import OrderedDict

from .fields import Field


class NodeMetaclass(type):
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

        return super(NodeMetaclass, mcs).__new__(mcs, name, bases, attrs)


class Node(object, metaclass=NodeMetaclass):
    @property
    def fields(self):
        if not hasattr(self, '_fields'):
            self._fields = OrderedDict()
            # Copy the field instances so that node instances have
            # isolated field instances that they can modify safely.
            declared_fields = copy.deepcopy(self._declared_fields)
            for name, field in declared_fields.items():
                self._fields[name] = field
                field.bind(name=name, node=self)
        return self._fields

    def get_value(self, data):
        ret = {}

        for name, field in self.fields.items():
            field_data = data.get(name)
            key = field_data.get('alias') or name
            value = field.get_value(
                arguments=field_data.get('arguments', {}),
                fields=field_data.get('fields', {}),
            )
            ret[key] = value

        return ret
