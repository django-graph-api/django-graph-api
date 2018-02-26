import pytest

from django_graph_api.graphql.schema import (
    DirectiveObject,
    DirectiveLocationEnum,
    EnumValueObject,
    FieldObject,
    InputValueObject,
    SchemaObject,
    TypeObject,
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
    NonNull)

from test_app.schema import (
    Character,
    Episode,
    schema,
)


def test_schema__get_types():
    schema_object = SchemaObject(None, schema.query_root, None)

    types = schema_object.get_types()
    assert types == [
        Character,
        Episode,
        schema.query_root,
        DirectiveObject,
        DirectiveLocationEnum,
        EnumValueObject,
        FieldObject,
        InputValueObject,
        SchemaObject,
        TypeObject,
        TypeKindEnum,
        Boolean,
        Int,
        String,
    ]


def test_type__scalar__get_fields():
    type_object = TypeObject(None, Boolean, None)
    assert type_object.get_fields() is None


def test_type__scalar__get_inputFields():
    type_object = TypeObject(None, Boolean, None)
    assert type_object.get_inputFields() is None


def test_type__scalar__get_interfaces():
    type_object = TypeObject(None, Boolean, None)
    assert type_object.get_interfaces() is None


def test_type__scalar__get_possibleTypes():
    type_object = TypeObject(None, Boolean, None)
    assert type_object.get_possibleTypes() is None


def test_type__scalar__get_enumValues():
    type_object = TypeObject(None, Boolean, None)
    assert type_object.get_enumValues() is None


def test_type__scalar__get_ofType():
    type_object = TypeObject(None, Boolean, None)
    assert type_object.get_ofType() is None


def test_type__non_null__get_fields():
    type_object = TypeObject(None, NonNull(Boolean), None)
    assert type_object.get_fields() is None


def test_type__non_null__get_inputFields():
    type_object = TypeObject(None, NonNull(Boolean), None)
    assert type_object.get_inputFields() is None


def test_type__non_null__get_interfaces():
    type_object = TypeObject(None, NonNull(Boolean), None)
    assert type_object.get_interfaces() is None


def test_type__non_null__get_possibleTypes():
    type_object = TypeObject(None, NonNull(Boolean), None)
    assert type_object.get_possibleTypes() is None


def test_type__non_null__get_enumValues():
    type_object = TypeObject(None, NonNull(Boolean), None)
    assert type_object.get_enumValues() is None


def test_type__non_null__get_ofType():
    type_object = TypeObject(None, NonNull(Boolean), None)
    assert type_object.get_ofType() is Boolean


def test_type__object__get_name():
    type_object = TypeObject(None, Character, None)
    assert type_object.get_name() == 'Character'
    type_object = TypeObject(None, TypeObject, None)
    assert type_object.get_name() == '__Type'


def test_type__object__get_fields():
    type_object = TypeObject(None, TypeObject, None)
    assert type_object.get_fields() == [
        ('description', TypeObject._declared_fields['description']),
        ('enumValues', TypeObject._declared_fields['enumValues']),
        ('fields', TypeObject._declared_fields['fields']),
        ('inputFields', TypeObject._declared_fields['inputFields']),
        ('interfaces', TypeObject._declared_fields['interfaces']),
        ('kind', TypeObject._declared_fields['kind']),
        ('name', TypeObject._declared_fields['name']),
        ('ofType', TypeObject._declared_fields['ofType']),
        ('possibleTypes', TypeObject._declared_fields['possibleTypes']),
    ]
    # Schema fields should be ignored.
    type_object = TypeObject(None, schema.query_root, None)
    assert type_object.get_fields() == [
        ('episode', schema.query_root._declared_fields['episode']),
        ('episodes', schema.query_root._declared_fields['episodes']),
        ('hero', schema.query_root._declared_fields['hero']),
    ]


def test_type__object__get_inputFields():
    type_object = TypeObject(None, TypeObject, None)
    assert type_object.get_inputFields() is None


def test_type__object__get_interfaces():
    type_object = TypeObject(None, TypeObject, None)
    assert type_object.get_interfaces() == []


def test_type__object__get_possibleTypes():
    type_object = TypeObject(None, TypeObject, None)
    assert type_object.get_possibleTypes() is None


def test_type__object__get_enumValues():
    type_object = TypeObject(None, TypeObject, None)
    assert type_object.get_enumValues() is None


def test_type__object__get_ofType():
    type_object = TypeObject(None, TypeObject, None)
    assert type_object.get_ofType() is None


def test_type__enum__get_fields():
    type_object = TypeObject(None, TypeKindEnum, None)
    assert type_object.get_fields() is None


def test_type__enum__get_inputFields():
    type_object = TypeObject(None, TypeKindEnum, None)
    assert type_object.get_inputFields() is None


def test_type__enum__get_interfaces():
    type_object = TypeObject(None, TypeKindEnum, None)
    assert type_object.get_interfaces() is None


def test_type__enum__get_possibleTypes():
    type_object = TypeObject(None, TypeKindEnum, None)
    assert type_object.get_possibleTypes() is None


def test_type__enum__get_enumValues():
    type_object = TypeObject(None, TypeKindEnum, None)
    assert type_object.get_enumValues() == TypeKindEnum.values


def test_type__enum__get_ofType():
    type_object = TypeObject(None, TypeKindEnum, None)
    assert type_object.get_ofType() is None


def test_type__list__get_name():
    type_object = TypeObject(None, List(Character), None)
    assert type_object.get_name() is None


def test_type__list__get_fields():
    type_object = TypeObject(None, List(Character), None)
    assert type_object.get_fields() is None


def test_type__list__get_inputFields():
    type_object = TypeObject(None, List(Character), None)
    assert type_object.get_inputFields() is None


def test_type__list__get_interfaces():
    type_object = TypeObject(None, List(Character), None)
    assert type_object.get_interfaces() is None


def test_type__list__get_possibleTypes():
    type_object = TypeObject(None, List(Character), None)
    assert type_object.get_possibleTypes() is None


def test_type__list__get_enumValues():
    type_object = TypeObject(None, List(Character), None)
    assert type_object.get_enumValues() is None


def test_type__list__get_ofType():
    type_object = TypeObject(None, List(Character), None)
    assert type_object.get_ofType() is Character


def test_field__get_type():
    field_object = FieldObject(
        None,
        ('name', CharField()),
        None,
    )
    assert field_object.get_type() == String
    field_object = FieldObject(
        None,
        ('characters', RelatedField('self')),
        None,
    )
    field_object.data[1]._self_object_type = Character
    assert field_object.get_type() == Character
    field_object = FieldObject(
        None,
        ('characters', RelatedField(Character)),
        None,
    )
    assert field_object.get_type() == Character
    field_object = FieldObject(
        None,
        ('characters', RelatedField(lambda: Character)),
        None,
    )
    assert field_object.get_type() == Character
    field_object = FieldObject(
        None,
        ('characters', RelatedField('test_app.schema.Character')),
        None,
    )
    assert field_object.get_type() == Character
    field_object = FieldObject(
        None,
        ('characters', ManyRelatedField(Character)),
        None,
    )
    assert field_object.get_type() == List(Character)


def test_field__get_type_exceptions():
    field_object = FieldObject(
        None,
        ('characters', RelatedField('test_app.schema.NonExistClass')),
        None,
    )
    with pytest.raises(ValueError):
        field_object.get_type()
    field_object = FieldObject(
        None,
        ('characters', RelatedField('NonExistModule.NonExistClass')),
        None,
    )
    with pytest.raises(ValueError):
        field_object.get_type()


def test_field__get_args():
    field_object = FieldObject(
        None,
        ('characters', ManyRelatedField(Character, arguments={'types': List(String)})),
        None,
    )
    assert field_object.get_args() == (('types', List(String)),)
    field_object = FieldObject(
        None,
        ('characters', ManyRelatedField(Episode, arguments={'types': Int()})),
        None,
    )
    assert field_object.get_args() == (('types', Int()),)


def test_inputvalue__get_name():
    inputvalue_object = InputValueObject(
        None,
        ('argname', String()),
        None,
    )
    assert inputvalue_object.get_name() == 'argname'


def test_inputvalue__get_type():
    inputvalue_object = InputValueObject(
        None,
        ('name', String()),
        None,
    )
    assert inputvalue_object.get_type() == String
    inputvalue_object = InputValueObject(
        None,
        ('names', List(String)),
        None,
    )
    assert inputvalue_object.get_type() == List(String)


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
    assert schema.execute(document) == {
        'data': {
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
            }
        }
    }


def test_execute__introspect_directives():
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
