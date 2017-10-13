from graphql.parser import GraphQLParser


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

    def register_query_root(self, query_root):
        self.query_root = query_root
        return query_root

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

        if any(selection.name == '__schema' for selection in query_ast.selections):
            raise NotImplementedError('This version of django-graph-api does not support introspection')

        return {
            'data': self.query_root(query_ast, None).serialize(),
        }


schema = Schema()
