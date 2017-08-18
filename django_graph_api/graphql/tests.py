from .fields import Field
from .nodes import Node
from .schema import Schema


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
