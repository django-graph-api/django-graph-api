from ..schema import schema


def test_hero_name():
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


def test_hero_name_and_friends_names():
    document = '''
    {
        hero {
            name
            friends {
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
            },
        }
    }


def test_hero_name_and_episodes():
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
