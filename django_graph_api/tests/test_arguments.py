from test_app.schema import schema


def test_episodes_and_characters(starwars_data):
    document = '''
        {
            episodes(number: 5) {
                name
                number
                characters(pk__gte: 2000) {
                    name
                }
            }
        }
        '''
    assert schema.execute(document) == {
        'data': {
            'episodes': [
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
