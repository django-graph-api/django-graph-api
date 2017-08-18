from django_graph_api.graphql.fields import Field
from django_graph_api.graphql.nodes import Node
from django_graph_api.graphql.schema import Schema


class WorldField(Field):
    def get_value(self, arguments=None, fields=None):
        return 'World'


class QueryNode(Node):
    hello = WorldField()


def test_execute_query():
    document = '''
    {
        hello
    }
    '''
    schema = Schema(
        query_node=QueryNode(),
    )
    assert schema.execute(document) == {'hello': 'World'}
