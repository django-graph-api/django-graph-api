from django_graph_api.graphql.request import Request
from django_graph_api.graphql.utils import GraphQLError
from test_app.schema import schema


def test_min_one_operation():
    document = '''
    fragment heroIdFragment on Character {
        id
        ...heroNameFragment
    }
    '''
    request = Request(document, schema)
    request.validate()
    assert request.errors == [
        GraphQLError("At least one operation must be provided"),
    ]


def test_named_operation__valid_document():
    document = '''
    query getDogName {
      dog {
        name
      }
    }

    query getOwnerName {
      dog {
        owner {
          name
        }
      }
    }
    '''
    request = Request(document, schema, operation_name='getDogName')
    request.validate()
    assert request.errors == []


def test_named_operation__uniqueness():
    document = '''
    query getName {
      dog {
        name
      }
    }

    query getName {
      dog {
        owner {
          name
        }
      }
    }
    '''
    request = Request(document, schema, operation_name='getName')
    request.validate()
    assert request.errors == [
        GraphQLError('Non-unique operation name: getName'),
    ]


def test_named_operation__uniqueness__different_types():
    document = '''
    query dogOperation {
      dog {
        name
      }
    }

    mutation dogOperation {
      mutateDog {
        id
      }
    }
    '''
    request = Request(document, schema, operation_name='dogOperation')
    request.validate()
    assert request.errors == [
        GraphQLError('Non-unique operation name: dogOperation'),
    ]


def test_anonymous_operation__valid_document():
    document = '''
    query {
      dog {
        name
      }
    }
    '''
    request = Request(document, schema)
    request.validate()
    assert request.errors == []


def test_anonymous_operation__max_one_anonymous_operation():
    document = '''
    {
      dog {
        name
      }
    }
    {
      dog {
        name
      }
    }
    '''
    request = Request(document, schema)
    request.validate()
    assert request.errors == [
        GraphQLError("Parse error: Line 7, col 5: Syntax error at '{'"),
    ]


def test_anonymous_operation__no_named_operations():
    document = '''
    {
      dog {
        name
      }
    }

    query getName {
      dog {
        owner {
          name
        }
      }
    }
    '''
    request = Request(document, schema)
    request.validate()
    assert request.errors == [
        GraphQLError("Parse error: Line 8: Syntax error at 'query'"),
    ]
