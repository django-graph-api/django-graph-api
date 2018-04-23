from django_graph_api.graphql.utils import GraphQLError
from django_graph_api.graphql.request import Request
from django_graph_api.graphql.schema import Schema

from test_app.schema import QueryRoot


def test_non_existent_episode(starwars_data):
    document = '''
        {
            episode (number: 12) {
                name
            }
        }
        '''
    request = Request(document)
    schema = Schema(query_root_classes=[QueryRoot])
    data, errors = schema.execute(request)
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
    request = Request(document)
    schema = Schema(query_root_classes=[QueryRoot])
    data, errors = schema.execute(request)
    assert data == {
        "episode": {
            "name": "A New Hope",
            "other_field": None
        }
    }
    assert errors == [
        GraphQLError('Episode does not have field other_field'),
    ]
