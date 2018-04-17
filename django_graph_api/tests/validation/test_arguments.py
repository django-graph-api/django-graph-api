from django_graph_api.graphql.request import Request
from django_graph_api.graphql.schema import Schema
from django_graph_api.graphql.utils import GraphQLError
from test_app.schema import QueryRoot


def test_non_null_scalar():
    document = '''
    {
        episode(number: null) {
            name
        }
    }
    '''
    request = Request(document)
    schema = Schema(QueryRoot)
    errors = schema.validate(request)
    assert errors == [
        GraphQLError("Required argument 'number' on 'episode' cannot be null"),
    ]


def test_missing_required_scalar():
    document = '''
    {
        episode {
            name
        }
    }
    '''
    request = Request(document)
    schema = Schema(QueryRoot)
    errors = schema.validate(request)
    assert errors == [
        GraphQLError("Required argument 'number' on 'episode' is missing"),
    ]


def test_non_null_list():
    document = '''
    {
        episode (number: 4) {
            characters (types: [null]) {
                name
            }
        }
    }
    '''
    request = Request(document)
    schema = Schema(QueryRoot)
    errors = schema.validate(request)
    assert errors == [
        GraphQLError("Argument 'types' on 'characters' cannot include null"),
    ]
