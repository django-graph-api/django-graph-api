import pytest

from test_app.schema import schema


def test_blank_query(starwars_data):
    query = ''
    # this needs to be updated with a more specific error,
    # when we implement the graphql errors
    with pytest.raises(Exception):
        schema.execute(query)
