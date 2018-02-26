from django_graph_api.graphql.utils import GraphQLError
from django_graph_api.graphql.request import Request

from test_app.schema import QueryRoot


def test_blank_query(starwars_data):
    document = ''
    request = Request(
        document=document,
        query_root_class=QueryRoot,
    )
    data, errors = request.execute()
    assert data is None
    assert errors == [
        'Parse error: Unexpected end of input',
    ]


def test_non_existent_episode(starwars_data):
    document = '''
        {
            episode (number: 12) {
                name
            }
        }
        '''
    request = Request(
        document=document,
        query_root_class=QueryRoot,
    )
    data, errors = request.execute()
    assert data == {
        "episode": None
    }
    assert errors == [
        GraphQLError('Error resolving episode: Episode matching query does not exist.'),
    ]


def test_non_existent_field(starwars_data):
    document = '''
        {
            episode (number: 4) {
                name
                other_field
            }
        }
        '''
    request = Request(
        document=document,
        query_root_class=QueryRoot,
    )
    data, errors = request.execute()
    assert data == {
        "episode": {
            "name": "A New Hope",
            "other_field": None
        }
    }
    assert errors == [
        GraphQLError('Episode does not have field other_field'),
    ]


def test_no_operations(starwars_data):
    document = '''
        fragment heroIdFragment on Character {
            id
            ...heroNameFragment
        }
        '''
    request = Request(
        document=document,
        query_root_class=QueryRoot,
    )
    data, errors = request.execute()
    assert data is None
    assert errors == [
        "At least one operation must be provided",
    ]
