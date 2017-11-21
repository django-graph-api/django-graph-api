from test_app.schema import schema


def test_episodes_and_characters_with_argument(starwars_data):
    document = '''
        {
            episode(number: 5) {
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
