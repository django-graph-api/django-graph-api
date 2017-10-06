from graphql.parser import GraphQLParser


class Schema(object):
    def __init__(self):
        self.query_root = None

    def register_query_root(self, query_root):
        self.query_root = query_root
        return query_root

    def execute(self, document):
        parser = GraphQLParser()
        ast = parser.parse(document)

        query_ast = ast.definitions[0]

        if any(selection.name == '__schema' for selection in query_ast.selections):
            raise NotImplementedError('This version of django-graph-api does not support introspection')

        return {
            'data': self.query_root(query_ast, None).serialize(),
        }


schema = Schema()
