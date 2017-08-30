from django_graph_api.graphql.schema import Schema
from django_graph_api.graphql.types import IntegerField, Object

schema = Schema()


# http://facebook.github.io/graphql/#sec-Scalars

def test_coerce_integer_result_from_string():
    @schema.register_query_root
    class QueryRoot(Object):
        result = IntegerField()

        def get_result(self):
            return '4'

    document = '''
    {
        result
    }
    '''
    assert schema.execute(document) == {
        'data': {
            'result': 4
        }
    }


def test_coerce_integer_result_from_float():
    @schema.register_query_root
    class QueryRoot(Object):
        result = IntegerField()

        def get_result(self):
            return 4.6

    document = '''
    {
        result
    }
    '''
    assert schema.execute(document) == {
        'data': {
            'result': 4
        }
    }


def test_coerce_integer_result_from_bool():
    @schema.register_query_root
    class QueryRoot(Object):
        result = IntegerField()

        def get_result(self):
            return False

    document = '''
    {
        result
    }
    '''
    assert schema.execute(document) == {
        'data': {
            'result': 0
        }
    }


def test_cannot_coerce_integer_result():
    @schema.register_query_root
    class QueryRoot(Object):
        result = IntegerField()

        def get_result(self):
            return 'abc'

    document = '''
    {
        result
    }
    '''

    assert schema.execute(document) == {
        'data': {
            'result': None
        }
    }

