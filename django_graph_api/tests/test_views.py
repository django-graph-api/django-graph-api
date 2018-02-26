from unittest import mock
import json

from django.http import JsonResponse
from django.template.response import TemplateResponse
from django.test import Client, modify_settings

from test_app.schema import QueryRoot


def test_get_request_graphiql():
    client = Client()
    response = client.get(
        '/graphql',
    )
    assert isinstance(response, TemplateResponse)
    assert response.status_code == 200
    assert response.templates[0].name == 'django_graph_api/graphiql.html'
    assert 'csrftoken' in response.cookies


@mock.patch('django_graph_api.views.Request')
def test_post_request_executed(Request):
    request = mock.MagicMock()
    request.execute.return_value = {}
    request.is_valid.return_value = True
    Request.return_value = request
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
    assert response.content == b'{}'
    Request.assert_called_once_with(
        document=query,
        variables=None,
        query_root_class=QueryRoot,
        operation_name=None,
    )
    request.execute.assert_called_once_with()


@mock.patch('django_graph_api.views.Request')
def test_variables_sent_in_post(Request):
    request = mock.MagicMock()
    request.execute.return_value = {}
    request.is_valid.return_value = True
    Request.return_value = request
    query = 'this is totally a query'
    client = Client()
    response = client.post(
        '/graphql',
        json.dumps({
            'query': query,
            'variables': {
                'level': 9001
            }
        }),
        content_type='application/json',
        HTTP_ACCEPT='application/json',
    )
    assert isinstance(response, JsonResponse)
    assert response.status_code == 200
    assert response.content == b'{}'
    Request.assert_called_once_with(
        document=query,
        variables={'level': 9001},
        query_root_class=QueryRoot,
        operation_name=None,
    )
    request.execute.assert_called_once_with()


def test_post_request_not_json():
    client = Client()
    response = client.post(
        '/graphql',
        '',
        content_type='application/json',
        HTTP_ACCEPT='application/json',
    )
    assert isinstance(response, JsonResponse)
    assert response.status_code == 200
    response_json = json.loads(response.content.decode('utf-8'))
    assert 'data must be json' in response_json['errors'][0]['message'].lower()


def test_post_request_without_query():
    client = Client()
    response = client.post(
        '/graphql',
        '',
        content_type='application/json',
        HTTP_ACCEPT='application/json',
    )
    assert isinstance(response, JsonResponse)
    assert response.status_code == 200
    response_json = json.loads(response.content.decode('utf-8'))
    assert '"query" key' in response_json['errors'][0]['message'].lower()


@modify_settings(MIDDLEWARE={'remove': 'django.middleware.csrf.CsrfViewMiddleware'})
@mock.patch('django_graph_api.views.Request')
def test_post__csrf_required(Request):
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
    Request.execute.assert_not_called()
