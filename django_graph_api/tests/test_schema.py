from django.core.exceptions import ImproperlyConfigured
import pytest

from django_graph_api.graphql.schema import (
    CombinedQueryRoot,
    IntrospectionQueryRoot,
    Schema,
)
from django_graph_api.graphql.types import (
    CharField,
    Object,
)


class NameQueryRootOne(Object):
    name = CharField()

    def get_name(self):
        pass


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


def test_combined_query_root_delegates_resolver():
    class QueryRoot(CombinedQueryRoot):
        query_root_classes = [NameQueryRootOne]

    query_root = QueryRoot(None, None, None)
    name_query_root = query_root.query_roots[0]

    assert query_root.get_name == name_query_root.get_name


def test_combined_query_root_delegates_resolver__nonexistant_field():
    class QueryRoot(CombinedQueryRoot):
        query_root_classes = [NameQueryRootOne]

    query_root = QueryRoot(None, None, None)

    with pytest.raises(AttributeError):
        query_root.get_thought


def test_combined_query_root_delegates_resolver__nonexistant_resolver():
    class QueryRoot(CombinedQueryRoot):
        query_root_classes = [NameQueryRootTwo]

    query_root = QueryRoot(None, None, None)

    with pytest.raises(AttributeError):
        query_root.get_name


def test_combined_query_root_accessing_missing_attribute():
    class QueryRoot(CombinedQueryRoot):
        query_root_classes = [NameQueryRootTwo]

    query_root = QueryRoot(None, None, None)

    with pytest.raises(AttributeError):
        query_root.missing_attribute
