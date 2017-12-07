from test_app.schema import schema


def test_episode_and_characters(starwars_data):
    document = '''
        {
            episode(number: 5) {
                name
                number
                characters (type: ["human", "droid"]) {
                    name
                }
            }
        }
        '''
    assert schema.execute(document) == {
        'data': {
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
                ]
            },
        }
    }


def test_episodes_and_droids(starwars_data):
    document = '''
        {
            episodes {
                name
                number
                characters (types: "droid") {
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
    }
