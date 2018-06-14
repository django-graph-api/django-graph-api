from django_graph_api.graphql.request import Request
from django_graph_api.graphql.schema import Schema
from django_graph_api.graphql.types import (
    CharField,
    Int,
    List,
    Object,
)
from django_graph_api.graphql.utils import GraphQLError
from test_app.schema import schema


def test_null_scalar():
    document = '''
    {
        episode(number: null) {
            name
        }
    }
    '''
    request = Request(document, schema)
    request.validate()
    assert request.errors == [
        GraphQLError("Non-null argument 'number' on 'episode' is null"),
    ]


def test_missing_scalar():
    document = '''
    {
        episode {
            name
        }
    }
    '''
    request = Request(document, schema)
    request.validate()
    assert request.errors == [
        GraphQLError("Required argument 'number' on 'episode' is missing"),
    ]


def test_related_object_args():
    document = '''
    {
        episode (number: 4) {
            characters (types: [null]) {
                name
            }
        }
    }
    '''
    request = Request(document, schema)
    request.validate()
    assert request.errors == [
        GraphQLError("Non-null argument 'types' on 'characters' is null"),
    ]

    document = '''
    {
        episode (number: 4) {
            characters {
                appears_in {
                    characters(types: [null]) {
                        name
                    }
                }
            }
        }
    }
    '''
    request = Request(document, schema)
    request.validate()
    assert request.errors == [
        GraphQLError("Non-null argument 'types' on 'characters' is null"),
    ]


class QueryRootWithNestedArgs(Object):
    nested = CharField(arguments={'arg': List(List(Int(null=False), null=False), null=False)})

    def get_nested(self, arg):
        return 1


test_schema = Schema(QueryRootWithNestedArgs)


def test_missing_arg():
    document = '''
    {
        nested
    }
    '''
    request = Request(document, test_schema)
    request.validate()
    assert request.errors == [
        GraphQLError("Required argument 'arg' on 'nested' is missing")
    ]


def test_empty_list():
    document = '''
    {
        nested(arg: [])
    }
    '''
    request = Request(document, test_schema)
    request.validate()
    assert request.errors == [
        GraphQLError("Non-null argument 'arg' on 'nested' is null")
    ]


def test_null_list_item():
    document = '''
    {
        nested(arg: [null])
    }
    '''
    request = Request(document, test_schema)
    request.validate()
    assert request.errors == [
        GraphQLError("Non-null argument 'arg' on 'nested' is null"),
    ]


def test_missing_int():
    document = '''
    {
        nested(arg: [[]])
    }
    '''
    request = Request(document, test_schema)
    request.validate()
    assert request.errors == [
        GraphQLError("Non-null argument 'arg' on 'nested' is null"),
    ]


def test_null_int():
    document = '''
    {
        nested(arg: [[null]])
    }
    '''
    request = Request(document, test_schema)
    request.validate()
    assert request.errors == [
        GraphQLError("Non-null argument 'arg' on 'nested' is null"),
    ]

    document = '''
    query nestedArgQuery($int: Int){
        nested(arg: [[$int]])
    }
    '''
    variables = {'int': None}

    request = Request(document, test_schema, variables=variables)
    request.validate()
    assert request.errors == [
        GraphQLError("Non-null argument 'arg' on 'nested' is null"),
    ]


def test_valid_input():
    document = '''
    {
        nested(arg: [[1]])
    }
    '''
    request = Request(document, test_schema)
    errors = request.validate()
    assert errors is None
