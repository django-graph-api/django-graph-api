from test_app.schema import schema


def test_blank_query(starwars_data):
    query = ''
    assert schema.execute(query) == {
        'errors': [
            {
                'type': 'Parse error',
                'message': 'Unexpected end of input'
            }
        ]
    }
