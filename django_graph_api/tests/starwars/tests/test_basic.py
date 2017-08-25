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
