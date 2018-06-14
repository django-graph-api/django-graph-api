from django_graph_api.graphql.request import Request

from test_app.schema import schema


def test_episode_name_field_description(starwars_data):
    document = """
    query IntrospectionQuery {
      __schema {
        queryType { name }
        mutationType { name }
        types {
          ...FullType
        }
        directives {
          name
          description
          locations
          args {
            ...InputValue
          }
        }
      }
    }

    fragment FullType on __Type {
      kind
      name
      description
      fields(includeDeprecated: true) {
        name
        description
        args {
          ...InputValue
        }
        type {
          ...TypeRef
        }
        isDeprecated
        deprecationReason
      }
      inputFields {
        ...InputValue
      }
      interfaces {
        ...TypeRef
      }
      enumValues(includeDeprecated: true) {
        name
        description
        isDeprecated
        deprecationReason
      }
      possibleTypes {
        ...TypeRef
      }
    }

    fragment InputValue on __InputValue {
      name
      description
      type { ...TypeRef }
      defaultValue
    }

    fragment TypeRef on __Type {
      kind
      name
      ofType {
        kind
        name
        ofType {
          kind
          name
          ofType {
            kind
            name
            ofType {
              kind
              name
              ofType {
                kind
                name
                ofType {
                  kind
                  name
                  ofType {
                    kind
                    name
                  }
                }
              }
            }
          }
        }
      }
    }"""
    request = Request(document, schema)
    data, errors = request.execute()
    assert errors == []
    types = data['__schema']['types']
    episodes = [type_ for type_ in types if type_['name'] == 'Episode'][0]
    name_field = [
        field for field in episodes['fields']
        if field['name'] == 'name'
    ][0]
    assert name_field['description'] == 'The name of an episode'


def test_episode_and_characters(starwars_data):
    document = '''
        {
            episode(number: 5) {
                name
                number
                characters (types: ["human", "droid"]) {
                    name
                }
            }
        }
        '''
    request = Request(document, schema)
    data, errors = request.execute()
    assert data == {
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
    assert errors == []


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
    request = Request(document, schema)
    data, errors = request.execute()
    assert data == {
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
    assert errors == []
