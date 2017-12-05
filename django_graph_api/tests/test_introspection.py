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
                        'name': 'Character',
                        'kind': 'OBJECT',
                        'fields': [
                            {
                                'name': 'appears_in'
                            },
                            {
                                'name': 'best_friend'
                            },
                            {
                                'name': 'friends'
                            },
                            {
                                'name': 'id',
                            },
                            {
                                'name': 'name'
                            },
                        ],
                    },
                    {
                        'name': 'Episode',
                        'kind': 'OBJECT',
                        'fields': [
                            {
                                'name': 'characters'
                            },
                            {
                                'name': 'name'
                            },
                            {
                                'name': 'next'
                            },
                            {
                                'name': 'number'
                            },
                        ],
                    },
                    {
                        'name': 'Boolean',
                        'kind': 'SCALAR',
                        'fields': None,
                    },
                    {
                        'name': 'Int',
                        'kind': 'SCALAR',
                        'fields': None,
                    },
                    {
                        'name': 'String',
                        'kind': 'SCALAR',
                        'fields': None,
                    },
                    {
                        'name': '__Directive',
                        'kind': 'OBJECT',
                        'fields': [
                            {
                                'name': 'args',
                            },
                            {
                                'name': 'description',
                            },
                            {
                                'name': 'locations',
                            },
                            {
                                'name': 'name',
                            },
                        ],
                    },
                    {
                        'name': '__DirectiveLocation',
                        'kind': 'ENUM',
                        'fields': [
                            {
                                'name': 'description',
                            },
                            {
                                'name': 'enumValues',
                            },
                            {
                                'name': 'fields',
                            },
                            {
                                'name': 'inputFields',
                            },
                            {
                                'name': 'interfaces',
                            },
                            {
                                'name': 'kind',
                            },
                            {
                                'name': 'name',
                            },
                        ],
                    },
                    {
                        'name': '__EnumValue',
                        'kind': 'OBJECT',
                        'fields': [
                            {
                                'name': 'description',
                            },
                            {
                                'name': 'name',
                            },
                            {
                                'name': 'isDeprecated',
                            },
                            {
                                'name': 'deprecationReason',
                            },
                        ],
                    },
                    {
                        'name': '__Field',
                        'kind': 'OBJECT',
                        'fields': [
                            {
                                'name': 'description'
                            },
                            {
                                'name': 'name'
                            },
                            {
                                'name': 'type'
                            },
                        ],
                    },
                    {
                        'name': '__InputValue',
                        'kind': 'OBJECT',
                        'fields': [
                            {
                                'name': 'defaultValue',
                            },
                            {
                                'name': 'description',
                            },
                            {
                                'name': 'name',
                            },
                            {
                                'name': 'type',
                            },
                        ],
                    },
                    {
                        'name': '__Schema',
                        'kind': 'OBJECT',
                        'fields': [
                            {
                                'name': 'directives',
                            },
                            {
                                'name': 'mutationType',
                            },
                            {
                                'name': 'queryType',
                            },
                            {
                                'name': 'types',
                            },
                        ],
                    },
                    {
                        'name': '__Type',
                        'kind': 'OBJECT',
                        'fields': [
                            {
                                'name': 'description',
                            },
                            {
                                'name': 'enumValues',
                            },
                            {
                                'name': 'fields',
                            },
                            {
                                'name': 'inputFields',
                            },
                            {
                                'name': 'interfaces',
                            },
                            {
                                'name': 'kind',
                            },
                            {
                                'name': 'name',
                            },
                        ],
                    },
                    {
                        'name': '__Type',
                        'kind': 'ENUM',
                        'fields': [
                            {
                                'name': 'description',
                            },
                            {
                                'name': 'enumValues',
                            },
                            {
                                'name': 'fields',
                            },
                            {
                                'name': 'inputFields',
                            },
                            {
                                'name': 'interfaces',
                            },
                            {
                                'name': 'kind',
                            },
                            {
                                'name': 'name',
                            },
                        ],
                    },
                ],
            },
        },
    }


def test_introspect_directives():
    document = '''{
        __schema {
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
    '''
    assert schema.execute(document) == {
        'data': {
            '__schema': {
                'directives': [],
            },
        },
    }
