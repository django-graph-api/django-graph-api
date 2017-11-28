from test_app.schema import schema


def test_introspect_types_and_fields():
    document = '''{
        __schema {
            types {
                name
                kind
                fields {
                    name
                }
            }
        }
    }
    '''
    assert schema.execute(document) == {
        'data': {
            '__schema': {
                'types': [
                    {
                        "name": "Character",
                        "kind": "OBJECT",
                        "fields": [
                            {
                                "name": "appears_in"
                            },
                            {
                                "name": "best_friend"
                            },
                            {
                                "name": "friends"
                            },
                            {
                                'name': 'id',
                            },
                            {
                                "name": "name"
                            },
                        ],
                    },
                    {
                        "name": "Episode",
                        "kind": "OBJECT",
                        "fields": [
                            {
                                "name": "characters"
                            },
                            {
                                "name": "name"
                            },
                            {
                                "name": "next"
                            },
                            {
                                "name": "number"
                            },
                        ],
                    },
                    {
                        "name": "Int",
                        "kind": "SCALAR",
                        "fields": None,
                    },
                    {
                        "name": "String",
                        "kind": "SCALAR",
                        "fields": None,
                    },
                    {
                        "name": "__Field",
                        "kind": "OBJECT",
                        "fields": [
                            {
                                "name": "description"
                            },
                            {
                                "name": "name"
                            },
                            {
                                "name": "type"
                            },
                        ],
                    },
                    {
                        "name": "__Schema",
                        "kind": "OBJECT",
                        "fields": [
                            {
                                "name": "mutationType"
                            },
                            {
                                "name": "queryType"
                            },
                            {
                                "name": "types"
                            },
                        ],
                    },
                    {
                        "name": "__Type",
                        "kind": "OBJECT",
                        "fields": [
                            {
                                "name": "description"
                            },
                            {
                                "name": "fields"
                            },
                            {
                                "name": "kind"
                            },
                            {
                                "name": "name"
                            },
                        ],
                    },
                ],
            },
        },
    }
