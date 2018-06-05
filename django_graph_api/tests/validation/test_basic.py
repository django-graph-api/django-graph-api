from django_graph_api.graphql.request import Request
from django_graph_api.graphql.utils import GraphQLError
from test_app.schema import schema


def test_blank_query(starwars_data):
    document = ''
    request = Request(document, schema)
    assert request.errors == [
        GraphQLError('Must provide query string.'),
    ]
