from test_app.schema import schema


def test_hero_name(starwars_data):
    document = '''
    {
        hero {
            name
        }
    }
    '''
    assert schema.execute(document) == {
        'data': {
            'hero': {
                'name': 'R2-D2',
            },
        }
    }


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
    assert schema.execute(document) == {
        'data': {
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
    }


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
    assert schema.execute(document) == {
        'data': {
            'hero': {
                'name': 'R2-D2',
                'appears_in': [{
                    'name': 'A New Hope',
                    'number': 4
                }]
            },
        }
    }


def test_episodes_and_characters(starwars_data):
    document = '''
        {
            episodes {
                name
                number
                characters {
                    name
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
                    'characters': [
                        {'name': 'Luke Skywalker'},
                        {'name': 'Darth Vader'},
                        {'name': 'Han Solo'},
                        {'name': 'Leia Organa'},
                        {'name': 'C-3PO'},
                        {'name': 'R2-D2'},
                    ]
                },
            ]
        }
    }
