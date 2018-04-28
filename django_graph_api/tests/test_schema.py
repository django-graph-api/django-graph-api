from django.core.exceptions import ImproperlyConfigured
import pytest

from django_graph_api.graphql.schema import (
    IntrospectionQueryRoot,
    Schema,
)
from django_graph_api.graphql.types import (
    CharField,
    Object,
)


class NameQueryRootOne(Object):
    name = CharField()


class NameQueryRootTwo(Object):
    name = CharField()


class ThoughtQueryRoot(Object):
    thought = CharField()


def test_instrospection_always_enabled():
    schema = Schema()
    assert '__schema' in schema.query_root_class._declared_fields
    assert '__type' in schema.query_root_class._declared_fields


def test_accepts_single_query_root():
    schema = Schema(NameQueryRootOne)
    assert schema.query_root_class.query_root_classes == [
        IntrospectionQueryRoot,
        NameQueryRootOne,
    ]
    assert set(schema.query_root_class._declared_fields) == (
        set(IntrospectionQueryRoot._declared_fields) |
        set(NameQueryRootOne._declared_fields)
    )


def test_accepts_multiple_query_roots():
    schema = Schema([NameQueryRootOne, ThoughtQueryRoot])
    assert schema.query_root_class.query_root_classes == [
        IntrospectionQueryRoot,
        NameQueryRootOne,
        ThoughtQueryRoot,
    ]
    assert set(schema.query_root_class._declared_fields) == (
        set(IntrospectionQueryRoot._declared_fields) |
        set(NameQueryRootOne._declared_fields) |
        set(ThoughtQueryRoot._declared_fields)
    )


def test_accepts_iterable():
    schema = Schema(
        query_root
        for query_root in [NameQueryRootOne, ThoughtQueryRoot]
    )
    assert schema.query_root_class.query_root_classes == [
        IntrospectionQueryRoot,
        NameQueryRootOne,
        ThoughtQueryRoot,
    ]
    assert set(schema.query_root_class._declared_fields) == (
        set(IntrospectionQueryRoot._declared_fields) |
        set(NameQueryRootOne._declared_fields) |
        set(ThoughtQueryRoot._declared_fields)
    )


def test_schema_detects_duplicate_fields():
    with pytest.raises(ImproperlyConfigured):
        Schema([NameQueryRootOne, NameQueryRootTwo])
