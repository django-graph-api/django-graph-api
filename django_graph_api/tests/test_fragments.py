from test_app.schema import schema


def test_fragments(starwars_data):
    document = '''
    {
        hero {
            ...heroFragment
        }
        episodes {
            ...episodeFragment
        }
    }

    fragment heroFragment on Character {
        id
        name
    }

    fragment episodeFragment on Episode {
        name
        number
    }
    '''
    assert schema.execute(document) == {
        'data': {
            'episodes': [
                {
                    'name': 'A New Hope',
                    'number': 4,
                },
            ],
            'hero': {
                'name': 'R2-D2',
                'id': 2001,
            },
        },
    }


def test_fragments__nested(starwars_data):
    document = '''
    {
        hero {
            ...heroIdFragment
        }
    }

    fragment heroIdFragment on Character {
        id
        ...heroNameFragment
    }

    fragment heroNameFragment on Character {
        name
    }
    '''
    assert schema.execute(document) == {
        'data': {
            'hero': {
                'name': 'R2-D2',
                'id': 2001,
            },
        },
    }


def test_fragments__inline(starwars_data):
    document = '''
    {
        hero {
            ... on Character {
                id
                name
            }
        }
        episodes {
            ... on Episode {
                name
                number
            }
        }
    }
    '''
    assert schema.execute(document) == {
        'data': {
            'episodes': [
                {
                    'name': 'A New Hope',
                    'number': 4,
                },
            ],
            'hero': {
                'name': 'R2-D2',
                'id': 2001,
            },
        },
    }
