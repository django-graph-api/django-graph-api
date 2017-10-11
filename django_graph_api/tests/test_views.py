from unittest import mock
import json

from django.http import JsonResponse
from django.template.response import TemplateResponse
from django.test import Client, modify_settings


def test_get_request_graphiql():
    client = Client()
    response = client.get(
        '/graphql',
    )
    assert isinstance(response, TemplateResponse)
    assert response.status_code == 200
    assert response.templates[0].name == 'django_graph_api/graphiql.html'
    assert 'csrftoken' in response.cookies


@mock.patch('test_project.urls.schema.execute')
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


@modify_settings(MIDDLEWARE={'remove': 'django.middleware.csrf.CsrfViewMiddleware'})
@mock.patch('test_project.urls.schema.execute')
def test_post__csrf_required(execute):
    execute.return_value = {}
    query = 'this is totally a query'
    client = Client(enforce_csrf_checks=True)
    response = client.post(
        '/graphql',
        json.dumps({
            'query': query,
        }),
        content_type='application/json',
        HTTP_ACCEPT='application/json',
    )
    assert response.status_code == 403
    execute.assert_not_called()
