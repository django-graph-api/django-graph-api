import pytest

from django_graph_api.graphql.introspection import (
    Directive,
    DirectiveLocationEnum,
    EnumValue,
    Field,
    InputValue,
    Schema as SchemaIntrospector,
    Type,
    TypeKindEnum,
)
from django_graph_api.graphql.types import (
    Boolean,
    CharField,
    Int,
    List,
    ManyRelatedField,
    RelatedField,
    String,
    NonNull,
    IntegerField,
)
from django_graph_api.graphql.request import Request

from test_app.schema import (
    Character,
    Episode,
    QueryRoot,
    schema,
)


def test_schema__get_types():
    schema_object = SchemaIntrospector(None, schema, None)

    types = schema_object.get_types()
    assert types == [
        Character,
        Episode,
        schema.query_root_class,
        Directive,
        DirectiveLocationEnum,
        EnumValue,
        Field,
        InputValue,
        SchemaIntrospector,
        Type,
        TypeKindEnum,
        Boolean,
        Int,
        String,
    ]


def test_type__scalar__get_fields():
    type_object = Type(None, Boolean, None)
    assert type_object.get_fields() is None


def test_type__scalar__get_inputFields():
    type_object = Type(None, Boolean, None)
    assert type_object.get_inputFields() is None


def test_type__scalar__get_interfaces():
    type_object = Type(None, Boolean, None)
    assert type_object.get_interfaces() is None


def test_type__scalar__get_possibleTypes():
    type_object = Type(None, Boolean, None)
    assert type_object.get_possibleTypes() is None


def test_type__scalar__get_enumValues():
    type_object = Type(None, Boolean, None)
    assert type_object.get_enumValues() is None


def test_type__scalar__get_ofType():
    type_object = Type(None, Boolean, None)
    assert type_object.get_ofType() is None


def test_type__non_null__get_fields():
    type_object = Type(None, NonNull(Boolean), None)
    assert type_object.get_fields() is None


def test_type__non_null__get_inputFields():
    type_object = Type(None, NonNull(Boolean), None)
    assert type_object.get_inputFields() is None


def test_type__non_null__get_interfaces():
    type_object = Type(None, NonNull(Boolean), None)
    assert type_object.get_interfaces() is None


def test_type__non_null__get_possibleTypes():
    type_object = Type(None, NonNull(Boolean), None)
    assert type_object.get_possibleTypes() is None


def test_type__non_null__get_enumValues():
    type_object = Type(None, NonNull(Boolean), None)
    assert type_object.get_enumValues() is None


def test_type__non_null__get_ofType():
    type_object = Type(None, NonNull(Boolean), None)
    assert type_object.get_ofType() == Boolean
    type_object = Type(None, NonNull(List(Boolean)), None)
    assert type_object.get_ofType() == List(Boolean)


def test_type__object__get_name():
    type_object = Type(None, Character, None)
    assert type_object.get_name() == 'Character'
    type_object = Type(None, Type, None)
    assert type_object.get_name() == '__Type'


def test_type__object__get_fields():
    type_object = Type(None, Type, None)
    assert type_object.get_fields() == [
        ('description', Type._declared_fields['description']),
        ('enumValues', Type._declared_fields['enumValues']),
        ('fields', Type._declared_fields['fields']),
        ('inputFields', Type._declared_fields['inputFields']),
        ('interfaces', Type._declared_fields['interfaces']),
        ('kind', Type._declared_fields['kind']),
        ('name', Type._declared_fields['name']),
        ('ofType', Type._declared_fields['ofType']),
        ('possibleTypes', Type._declared_fields['possibleTypes']),
    ]
    # Schema fields should be ignored.
    type_object = Type(None, QueryRoot, None)
    assert type_object.get_fields() == [
        ('episode', QueryRoot._declared_fields['episode']),
        ('episodes', QueryRoot._declared_fields['episodes']),
        ('hero', QueryRoot._declared_fields['hero']),
    ]


def test_type__object__get_inputFields():
    type_object = Type(None, Type, None)
    assert type_object.get_inputFields() is None


def test_type__object__get_interfaces():
    type_object = Type(None, Type, None)
    assert type_object.get_interfaces() == []


def test_type__object__get_possibleTypes():
    type_object = Type(None, Type, None)
    assert type_object.get_possibleTypes() is None


def test_type__object__get_enumValues():
    type_object = Type(None, Type, None)
    assert type_object.get_enumValues() is None


def test_type__object__get_ofType():
    type_object = Type(None, Type, None)
    assert type_object.get_ofType() is None


def test_type__enum__get_fields():
    type_object = Type(None, TypeKindEnum, None)
    assert type_object.get_fields() is None


def test_type__enum__get_inputFields():
    type_object = Type(None, TypeKindEnum, None)
    assert type_object.get_inputFields() is None


def test_type__enum__get_interfaces():
    type_object = Type(None, TypeKindEnum, None)
    assert type_object.get_interfaces() is None


def test_type__enum__get_possibleTypes():
    type_object = Type(None, TypeKindEnum, None)
    assert type_object.get_possibleTypes() is None


def test_type__enum__get_enumValues():
    type_object = Type(None, TypeKindEnum, None)
    assert type_object.get_enumValues() == TypeKindEnum.values


def test_type__enum__get_ofType():
    type_object = Type(None, TypeKindEnum, None)
    assert type_object.get_ofType() is None


def test_type__list__get_name():
    type_object = Type(None, List(Character), None)
    assert type_object.get_name() is None


def test_type__list__get_fields():
    type_object = Type(None, List(Character), None)
    assert type_object.get_fields() is None


def test_type__list__get_inputFields():
    type_object = Type(None, List(Character), None)
    assert type_object.get_inputFields() is None


def test_type__list__get_interfaces():
    type_object = Type(None, List(Character), None)
    assert type_object.get_interfaces() is None


def test_type__list__get_possibleTypes():
    type_object = Type(None, List(Character), None)
    assert type_object.get_possibleTypes() is None


def test_type__list__get_enumValues():
    type_object = Type(None, List(Character), None)
    assert type_object.get_enumValues() is None


def test_type__list__get_ofType():
    type_object = Type(None, List(Character), None)
    assert type_object.get_ofType() == Character
    type_object = Type(None, List(Int(null=False)), None)
    assert type_object.get_ofType() == NonNull(Int())


def test_field__get_type():
    field_object = Field(
        None,
        ('name', CharField()),
        None,
    )
    assert field_object.get_type() == String
    field_object = Field(
        None,
        ('characters', RelatedField('self')),
        None,
    )
    field_object.data[1]._self_object_type = Character
    assert field_object.get_type() == Character
    field_object = Field(
        None,
        ('characters', RelatedField(Character)),
        None,
    )
    assert field_object.get_type() == Character
    field_object = Field(
        None,
        ('characters', RelatedField(lambda: Character)),
        None,
    )
    assert field_object.get_type() == Character
    field_object = Field(
        None,
        ('characters', RelatedField('test_app.schema.Character')),
        None,
    )
    assert field_object.get_type() == Character
    field_object = Field(
        None,
        ('characters', ManyRelatedField(Character)),
        None,
    )
    assert field_object.get_type() == List(Character)
    field_object = Field(
        None,
        ('characters', ManyRelatedField(Character, null=False)),
        None,
    )
    assert field_object.get_type() == NonNull(List(Character))
    field_object = Field(
        None,
        ('id', IntegerField(null=False)),
        None,
    )
    assert field_object.get_type() == NonNull(Int)


def test_field__get_type_exceptions():
    field_object = Field(
        None,
        ('characters', RelatedField('test_app.schema.NonExistClass')),
        None,
    )
    with pytest.raises(ValueError):
        field_object.get_type()
    field_object = Field(
        None,
        ('characters', RelatedField('NonExistModule.NonExistClass')),
        None,
    )
    with pytest.raises(ValueError):
        field_object.get_type()


def test_field__get_args():
    field_object = Field(
        None,
        ('characters', ManyRelatedField(Character, arguments={'types': List(String)})),
        None,
    )
    assert field_object.get_args() == (('types', List(String)),)
    field_object = Field(
        None,
        ('characters', ManyRelatedField(Character, arguments={'types': Int()})),
        None,
    )
    assert field_object.get_args() == (('types', Int()),)


def test_inputvalue__get_name():
    inputvalue_object = InputValue(
        None,
        ('argname', String()),
        None,
    )
    assert inputvalue_object.get_name() == 'argname'


def test_inputvalue__get_type():
    inputvalue_object = InputValue(
        None,
        ('name', String()),
        None,
    )
    assert inputvalue_object.get_type() == String
    inputvalue_object = InputValue(
        None,
        ('names', List(String)),
        None,
    )
    assert inputvalue_object.get_type() == List(String)
    inputvalue_object = InputValue(
        None,
        ('name', String(null=False)),
        None,
    )
    assert inputvalue_object.get_type() == NonNull(String())


def test_execute__filter_type():
    document = '''{
        __type (name: Character) {
            name
            kind
            fields {
                name
                type {
                    name
                    kind
                    ofType {
                        name
                        kind
                    }
                }
            }
        }
    }
    '''
    request = Request(document, schema)
    data, errors = request.execute()
    assert data == {
        '__type': {
            'name': 'Character',
            'kind': 'OBJECT',
            'fields': [
                {
                    'name': 'appears_in',
                    'type': {
                        'name': None,
                        'kind': 'LIST',
                        'ofType': {
                            'name': 'Episode',
                            'kind': 'OBJECT'
                        }
                    },
                },
                {
                    'name': 'best_friend',
                    'type': {
                        'name': 'Character',
                        'kind': 'OBJECT',
                        'ofType': None
                    },
                },
                {
                    'name': 'friends',
                    'type': {
                        'name': None,
                        'kind': 'LIST',
                        'ofType': {
                            'name': 'Character',
                            'kind': 'OBJECT'
                        }
                    },
                },
                {
                    'name': 'id',
                    'type': {
                        'name': None,
                        'kind': 'NON_NULL',
                        'ofType': {
                            'name': 'Int',
                            'kind': 'SCALAR'
                        }
                    },
                },
                {
                    'name': 'name',
                    'type': {
                        'name': 'String',
                        'kind': 'SCALAR',
                        'ofType': None
                    },
                },
            ],
        },
    }
    assert errors == []


def test_execute__introspect_directives():
    document = '''{
        __schema {
            directives {
                name
                description
                locations
            }
        }
    }
    '''
    request = Request(document, schema)
    data, errors = request.execute()
    assert data == {
        '__schema': {
            'directives': [],
        },
    }
    assert errors == []
