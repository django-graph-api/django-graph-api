from test_app.schema import schema


def test_blank_query(starwars_data):
    query = ''
    assert schema.execute(query) == {
        'errors': [
            {
                'message': 'Parse error: Unexpected end of input'
            }
        ]
    }


def test_non_existent_episode(starwars_data):
    document = '''
        {
            episode (number: 12) {
                name
            }
        }
        '''
    assert schema.execute(document) == {
        "data": {
            "episode": None
        },
        "errors": [
            {
                "message": "Error resolving episode: Episode matching query does not exist."
            }
        ]
    }


def test_non_existent_field(starwars_data):
    document = '''
        {
            episode (number: 4) {
                name
                other_field
            }
        }
        '''
    assert schema.execute(document) == {
        "data": {
            "episode": {
                "name": "A New Hope",
                "other_field": None
            }
        },
        "errors": [
            {
                "message": "Episode does not have field other_field"
            }
        ]
    }


def test_no_query(starwars_data):
    document = '''
        mutation MyMutation {
          episodes {
            name
          }
        }
        '''
    assert schema.execute(document) == {
        "errors": [
            {
                "message": "Document error: Exactly one query must be defined"
            }
        ]
    }
