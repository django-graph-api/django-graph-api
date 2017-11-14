import copy

from graphql.parser import GraphQLParser
from django_graph_api.graphql.types import (
    CharField,
    ManyRelatedField,
    Object,
    OBJECT,
    RelatedField,
)


class FieldObject(Object):
    # self.data will be an item from a declared fields dict
    object_name = '__Field'
    name = CharField()
    description = CharField()
    type = RelatedField(lambda: TypeObject)

    def get_name(self):
        return self.data[0]

    def get_description(self):
        return getattr(self.data[1], 'description', None)

    def get_type(self):
        return self.data[1].type_


class TypeObject(Object):
    # self.data will be an object or scalar
    object_name = '__Type'
    kind = CharField()
    name = CharField()
    description = CharField()
    fields = ManyRelatedField(FieldObject)

    def get_name(self):
        return getattr(self.data, 'object_name', self.data.__name__)

    def get_fields(self):
        if self.data.kind != OBJECT:
            return None
        return sorted(
            self.data._declared_fields.items(),
            key=lambda item: item[0],
        )


class SchemaObject(Object):
    # self.data will be the query_root.
    object_name = '__Schema'
    types = ManyRelatedField(TypeObject)
    queryType = RelatedField(TypeObject)
    mutationType = RelatedField(TypeObject)

    def _collect_types(self, object_type, types=None):
        if types is None:
            types = set()
        for field in object_type._declared_fields.values():
            if isinstance(field, RelatedField):
                new_object_type = field.resolve_object_type(field.object_type)
                if new_object_type == 'self':
                    continue
                if new_object_type in types:
                    continue
                types.add(new_object_type)
                self._collect_types(new_object_type, types)
            elif field.type_:
                types.add(field.type_)
        return types

    def _type_key(self, type_):
        object_name = getattr(type_, 'object_name', type_.__name__)
        return (
            object_name.startswith('__'),
            type_.kind,
            object_name,
        )

    def get_types(self):
        types = self._collect_types(self.data)
        return sorted(types, key=self._type_key)

    def get_queryType(self):
        return self.data

    def get_mutationType(self):
        return None


class Schema(object):
    """
    Required for a GraphQL API.

    A schema is a set of nodes and edges with at least one query root to access the rest of
    the schema.

    To use:
    ::

        schema = Schema()

        @schema.register_query_root
        class QueryRoot(Object):
            hello = CharField()

            def get_hello(self):
                return 'world'

    Each GraphQLView is mapped to a single schema.
    ::

        urlpatterns = [
            url(r'^graphql$', GraphQLView.as_view(schema=schema)),
        ]
    """
    def __init__(self):
        self.query_root = None

    def register_query_root(self, BaseQueryRoot):
        class QueryRoot(BaseQueryRoot):
            def get___schema(self):
                return self.__class__
        QueryRoot._declared_fields = copy.deepcopy(BaseQueryRoot._declared_fields)
        QueryRoot._declared_fields['__schema'] = RelatedField(SchemaObject)

        self.query_root = QueryRoot
        return QueryRoot

    def execute(self, document):
        """
        Queries the schema in python.

        :param document: A GraphQL query string
        :return: JSON of returned data or errors

        e.g.
        ::

            query = '''
            {
                users {
                    name
                }
            }
            '''
            schema.execute(query)

        Might return
        ::

            {
                "data": {
                    "users": [
                        {"name": "Buffy Summers"},
                        {"name": "Willow Rosenberg"},
                        {"name": "Xander Harris"}
                    ]
                }
            }
        """
        parser = GraphQLParser()
        ast = parser.parse(document)

        query_ast = ast.definitions[0]

        return {
            'data': self.query_root(query_ast, None).serialize(),
        }


schema = Schema()
