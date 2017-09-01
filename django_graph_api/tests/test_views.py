from unittest import mock
import json

from django.http import JsonResponse
from django.template.response import TemplateResponse
from django.test import Client


def test_get_request_graphiql():
    client = Client()
    response = client.get(
        '/graphql',
    )
    assert isinstance(response, TemplateResponse)
    assert response.status_code == 200
    assert response.templates[0].name == 'django_graph_api/graphiql.html'


@mock.patch('django_graph_api.tests.urls.schema.execute')
def test_post_request_executed(execute):
    execute.return_value = {}
    query = 'this is totally a query'
    client = Client()
    response = client.post(
        '/graphql',
        json.dumps({
            'query': query,
        }),
        content_type='application/json',
        HTTP_ACCEPT='application/json',
    )
    assert isinstance(response, JsonResponse)
    assert response.status_code == 200
    assert response.json() == {}
    execute.assert_called_once_with(query)
