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
        return {
            'data': self.query_root(ast.definitions[0], None).serialize(),
        }


schema = Schema()
