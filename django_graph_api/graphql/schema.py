from .parse import parse


class Schema(object):
    def __init__(self):
        self._registry = {
            'enums': [],
            'types': [],
            'type_kinds': [],
        }

    def register_type_kind(self, type_kind):
        self._registry['type_kinds'].append(type_kind)
        return type_kind

    def register_type(self, type_):
        self._registry['types'].append(type_)
        return type_

    def register_enum(self, enum):
        self._registry['enums'].append(enum)
        return enum

    def execute(self, document):
        parsed = parse(document)
        return self.query_node.get_value(data=parsed)


schema = Schema()
