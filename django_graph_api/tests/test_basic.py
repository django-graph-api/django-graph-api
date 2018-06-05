from django_graph_api.graphql.request import Request

from test_app.schema import schema


def test_hero_name(starwars_data):
    document = '''
    {
        hero {
            name
        }
    }
    '''
    request = Request(document, schema)
    data, errors = request.execute()
    assert data == {
        'hero': {
            'name': 'R2-D2',
        },
    }
    assert errors == []


def test_hero_name_and_friends_names(starwars_data):
    document = '''
    {
        hero {
            name
            friends {
                name
            }
            best_friend {
                name
            }
        }
    }
    '''
    request = Request(document, schema)
    data, errors = request.execute()
    assert data == {
        'hero': {
            'name': 'R2-D2',
            'friends': [
                {
                    'name': 'Luke Skywalker',
                },
                {
                    'name': 'Han Solo',
                },
                {
                    'name': 'Leia Organa',
                },
                {
                    'name': 'C-3PO',
                },
            ],
            'best_friend': {
                'name': 'Luke Skywalker'
            }
        },
    }
    assert errors == []


def test_hero_name_and_episodes(starwars_data):
    document = '''
    {
        hero {
            name
            appears_in {
                name
                number
            }
        }
    }
    '''
    request = Request(document, schema)
    data, errors = request.execute()
    assert data == {
        'hero': {
            'name': 'R2-D2',
            'appears_in': [
                {
                    'name': 'A New Hope',
                    'number': 4
                },
                {
                    'name': 'The Empire Strikes Back',
                    'number': 5
                },
            ]
        },
    }
    assert errors == []
