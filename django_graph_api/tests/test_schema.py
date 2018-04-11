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
    assert schema.query_root_classes == [IntrospectionQueryRoot]


def test_accepts_multiple_query_roots():
    schema = Schema([NameQueryRootOne, ThoughtQueryRoot])
    assert schema.query_root_classes == [
        IntrospectionQueryRoot,
        NameQueryRootOne,
        ThoughtQueryRoot,
    ]


def test_schema_detects_duplicate_fields():
    with pytest.raises(ImproperlyConfigured):
        Schema([NameQueryRootOne, NameQueryRootTwo])
