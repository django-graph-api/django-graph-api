from unittest import mock

from django.http import JsonResponse
from django.template.response import TemplateResponse
from django.test import Client


def test_get_request_graphiql():
    client = Client()
    response = client.get(
        '/graphql/',
    )
    assert isinstance(response, TemplateResponse)
    assert response.status_code == 200
    assert response.templates[0].name == 'django_graph_api/graphiql.html'


@mock.patch('django_graph_api.views.schema')
def test_post_request_executed(schema):
    schema.execute.return_value = {}
    query = 'this is totally a query'
    client = Client()
    response = client.post(
        '/graphql/',
        query,
        content_type='application/graphql',
        HTTP_ACCEPT='application/json',
    )
    assert isinstance(response, JsonResponse)
    assert response.status_code == 200
    assert response.json() == {}
    schema.execute.assert_called_once_with(query)
