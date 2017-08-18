from graphql.parser import GraphQLParser


class Schema(object):
    def __init__(self):
        self._registry = {
            'enums': [],
            'types': [],
            'type_kinds': [],
        }
        self.query_root = None

    def register_type_kind(self, type_kind):
        self._registry['type_kinds'].append(type_kind)
        return type_kind

    def register_type(self, type_):
        self._registry['types'].append(type_)
        return type_

    def register_enum(self, enum):
        self._registry['enums'].append(enum)
        return enum

    def register_query_root(self, query_root):
        self.query_root = query_root
        return query_root

    def execute(self, document):
        parser = GraphQLParser()
        ast = parser.parse(document)
        return {
            'data': self.query_root().serialize(),
        }


schema = Schema()
