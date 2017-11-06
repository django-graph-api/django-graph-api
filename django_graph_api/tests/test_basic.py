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
    }
