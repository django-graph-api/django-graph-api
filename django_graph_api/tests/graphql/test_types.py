from unittest.mock import patch

import pytest

from unittest import mock

from django_graph_api.graphql.types import (
    Boolean,
    BooleanField,
    CharField,
    Float,
    Int,
    List,
    String,
)


@patch('django_graph_api.graphql.types.Boolean.coerce_result')
def test_field_get_value_calls_coerce_result(coerce_result_mock):
    field = BooleanField()
    selection = mock.MagicMock()
    selection.name = 'foo'
    obj = mock.MagicMock()
    obj.get_foo.return_value = 'bar'
    field.bind(selection, obj)

    field.get_value()
    coerce_result_mock.assert_called_once_with('bar')


def test_boolean_coerce_result():
    assert Boolean.coerce_result(1) is True
    assert Boolean.coerce_result(None) is None


def test_int_coerce_result():
    assert Int.coerce_result(True) is 1
    assert Int.coerce_result(4.9) is 4
    assert Int.coerce_result(None) is None

    with pytest.raises(ValueError):
        Int.coerce_result('2.0')


def test_float_coerce_result():
    assert Float.coerce_result(-10) == -10.0
    assert Float.coerce_result(None) is None

    with pytest.raises(ValueError):
        Float.coerce_result('abc')


def test_string_coerce_result():
    assert String.coerce_result(True) == 'True'
    assert String.coerce_result(4.9) == '4.9'
    assert String.coerce_result(None) is None


def test_list_coerce_result():
    assert List(Boolean).coerce_result({False}) == [False]
    assert List(String).coerce_result([True]) == ['True']
    assert List(Int).coerce_result((1, 2, '3')) == [1, 2, 3]
    assert List(Int).coerce_result(None) is None
    assert List(String).coerce_result('not a list') == ['not a list']

    with pytest.raises(ValueError):
        List(Float).coerce_result(['not a float'])


@patch('django_graph_api.graphql.types.Boolean.coerce_input')
def test_field_get_value_calls_coerce_input(coerce_input_mock):
    field = CharField(foo=Boolean())
    selection = mock.MagicMock()
    argument = mock.Mock()
    argument.name = 'foo'
    argument.value = 'bar'
    selection.arguments = [argument]
    obj = mock.MagicMock()
    field.bind(selection, obj)

    field.get_resolver_args()
    coerce_input_mock.assert_called_once_with('bar')


def test_boolean_coerce_input():
    assert Boolean.coerce_input(1) is True
    assert Boolean.coerce_input(None) is None


def test_int_coerce_input():
    assert Int.coerce_input(-12) == -12
    assert Int.coerce_input(None) is None

    with pytest.raises(ValueError):
        Int.coerce_input('2')

    with pytest.raises(ValueError):
        Int.coerce_input(True)

    with pytest.raises(ValueError):
        Int.coerce_input(2.0)

    max_int = (2 ^ 31) - 1
    assert Int.coerce_input(max_int) == max_int

    with pytest.raises(ValueError):
        Int.coerce_input(max_int + 1)

    min_int = -2 ^ 31
    assert Int.coerce_input(min_int) == min_int
    with pytest.raises(ValueError):
        Int.coerce_input(min_int - 1)


def test_float_coerce_input():
    assert Float.coerce_input(-10) == -10.0
    assert Float.coerce_input(None) is None

    with pytest.raises(ValueError):
        Float.coerce_input('abc')


def test_string_coerce_input():
    assert String.coerce_input(True) == 'True'
    assert String.coerce_input(4.9) == '4.9'
    assert String.coerce_input(None) is None


def test_list_coerce_input():
    assert List(Int).coerce_input([]) == []
    assert List(Boolean).coerce_input({True}) == [True]
    assert List(Int).coerce_input((1, 2, 3)) == [1, 2, 3]
    assert List(String).coerce_input('123') == ['123']
    assert List(String).coerce_input(True) == ['True']
    assert List(Int).coerce_input(None) is None

    with pytest.raises(ValueError):
        List(Int).coerce_input(['1', '2'])
