import pytest

from test_app.schema import schema


def test_blank_query(starwars_data):
    query = ''
    with pytest.raises(Exception):
        schema.execute(query)
