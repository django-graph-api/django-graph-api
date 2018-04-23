from django_graph_api.graphql.request import Request
from django_graph_api.graphql.schema import Schema

from test_app.schema import QueryRoot


def test_query_default_episode_and_characters(starwars_data):
    document = '''
        query EpisodeAndCharacters($episode: ID = 5) {
            episode(number: $episode) {
                name
                number
                characters (type: ["human", "droid"]) {
                    name
                }
            }
        }
        '''
    request = Request(document=document)
    schema = Schema(query_root_classes=[QueryRoot])
    data, errors = schema.execute(request)
    assert data == {
        'episode': {
            'name': 'The Empire Strikes Back',
            'number': 5,
            'characters': [
                {'name': 'Luke Skywalker'},
                {'name': 'Darth Vader'},
                {'name': 'Han Solo'},
                {'name': 'Leia Organa'},
                {'name': 'C-3PO'},
                {'name': 'R2-D2'},
            ],
        },
    }
    assert errors == []


def test_query_missing_variable_no_default(starwars_data):
    document = '''
        query Episodes($episode: Int) {
            episodes(number: $episode) {
                number
            }
        }
        '''
    request = Request(document=document)
    schema = Schema(query_root_classes=[QueryRoot])
    data, errors = schema.execute(request)
    assert data == {
        'episodes': [{
            'number': 4,
        }, {
            'number': 5,
        }]
    }
    assert errors == []


def test_query_episodes_and_droids(starwars_data):
    document = '''
        query EpisodesAndCharacterType($type: String) {
            episodes {
                name
                number
                characters (types: $type) {
                    name
                }
            }
        }
        '''
    request = Request(document=document, variables={'type': 'droid'})
    schema = Schema(query_root_classes=[QueryRoot])
    data, errors = schema.execute(request)
    assert data == {
        'episodes': [
            {
                'name': 'A New Hope',
                'number': 4,
                'characters': [
                    {'name': 'C-3PO'},
                    {'name': 'R2-D2'},
                ]
            },
            {
                'name': 'The Empire Strikes Back',
                'number': 5,
                'characters': [
                    {'name': 'C-3PO'},
                    {'name': 'R2-D2'},
                ]
            },
        ]
    }
    assert errors == []
