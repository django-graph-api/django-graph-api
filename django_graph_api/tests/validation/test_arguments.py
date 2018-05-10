from django_graph_api.graphql.request import Request
from django_graph_api.graphql.schema import (
    Schema,
    BaseQueryRoot,
)
from django_graph_api.graphql.types import (
    CharField,
    List,
    Int,
)
from django_graph_api.graphql.utils import GraphQLError
from test_app.schema import QueryRoot


def test_null_scalar():
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
        GraphQLError("Argument 'number' on 'episode' is invalid"),
    ]


def test_missing_scalar():
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
    request = Request(document)
    schema = Schema(QueryRoot)
    errors = schema.validate(request)
    assert errors == [
        GraphQLError("Argument 'types' on 'characters' is invalid"),
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
    request = Request(document)
    errors = schema.validate(request)
    assert errors == [
        GraphQLError("Argument 'types' on 'characters' is invalid"),
    ]


class QueryRootWithNestedArgs(BaseQueryRoot):
    nested = CharField(arguments={'arg': List(List(Int(null=False), null=False), null=False)})

    def get_nested(self, arg):
        return 1


def test_missing_arg():
    document = '''
    {
        nested
    }
    '''
    request = Request(document)
    schema = Schema(QueryRootWithNestedArgs)
    errors = schema.validate(request)
    assert errors == [
        GraphQLError("Required argument 'arg' on 'nested' is missing")
    ]


def test_empty_list():
    document = '''
    {
        nested(arg: [])
    }
    '''
    request = Request(document)
    schema = Schema(QueryRootWithNestedArgs)
    errors = schema.validate(request)
    assert errors == [
        GraphQLError("Argument 'arg' on 'nested' is invalid")
    ]


def test_null_list_item():
    document = '''
    {
        nested(arg: [null])
    }
    '''
    request = Request(document)
    schema = Schema(QueryRootWithNestedArgs)
    errors = schema.validate(request)
    assert errors == [
        GraphQLError("Argument 'arg' on 'nested' is invalid"),
    ]


def test_missing_int():
    document = '''
    {
        nested(arg: [[]])
    }
    '''
    request = Request(document)
    schema = Schema(QueryRootWithNestedArgs)
    errors = schema.validate(request)
    assert errors == [
        GraphQLError("Argument 'arg' on 'nested' is invalid"),
    ]


def test_null_int():
    document = '''
    {
        nested(arg: [[null]])
    }
    '''
    request = Request(document)
    schema = Schema(QueryRootWithNestedArgs)
    errors = schema.validate(request)
    assert errors == [
        GraphQLError("Argument 'arg' on 'nested' is invalid"),
    ]

    document = '''
    query nestedArgQuery($int: Int){
        nested(arg: [[$int]])
    }
    '''
    variables = {'int': None}

    request = Request(document, variables)
    errors = schema.validate(request)
    assert errors == [
        GraphQLError("Argument 'arg' on 'nested' is invalid"),
    ]


def test_valid_input():
    document = '''
    {
        nested(arg: [[1]])
    }
    '''
    request = Request(document)
    schema = Schema(QueryRootWithNestedArgs)
    errors = schema.validate(request)
    assert errors is None
