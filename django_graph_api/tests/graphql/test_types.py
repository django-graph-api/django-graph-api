import pytest

from unittest import mock

from django_graph_api.graphql.schema import Schema
from django_graph_api.graphql.types import Boolean, Float, Field, Int, String, List

schema = Schema()


def test_field_get_value_calls_coerce():
    field = Field()
    field.type_ = mock.Mock()
    field.name = 'foo'
    field.obj = mock.Mock()
    field.obj.get_foo.return_value = 'bar'

    field.get_value()
    field.type_.coerce_result.assert_called_once_with('bar')


def test_boolean_coerce():
    assert Boolean.coerce_result(1) is True
    assert Boolean.coerce_result(None) is None


def test_int_coerce():
    assert Int.coerce_result(True) is 1
    assert Int.coerce_result(4.9) is 4
    assert Int.coerce_result(None) is None

    with pytest.raises(ValueError):
        Int.coerce_result('2.0')


def test_float_coerce():
    assert Float.coerce_result(-10) == -10.0
    assert Float.coerce_result(None) is None

    with pytest.raises(ValueError):
        Float.coerce_result('abc')


def test_string_coerce():
    assert String.coerce_result(True) == 'True'
    assert String.coerce_result(4.9) == '4.9'
    assert String.coerce_result(None) is None


def test_list_coerce():
    assert List.coerce_result({True}) == [True]
    assert List.coerce_result((1, 2, 3)) == [1, 2, 3]
    assert List.coerce_result(None) is None
