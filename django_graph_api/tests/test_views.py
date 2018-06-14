from unittest import mock
import json

from django.http import JsonResponse
from django.template.response import TemplateResponse
from django.test import Client, modify_settings

from django_graph_api.graphql.request import Request
from test_app.schema import schema


def test_get_request_graphiql():
    client = Client()
    response = client.get(
        '/graphql',
    )
    assert isinstance(response, TemplateResponse)
    assert response.status_code == 200
    assert response.templates[0].name == 'django_graph_api/graphiql.html'
    assert 'csrftoken' in response.cookies


@mock.patch('django_graph_api.views.Request', wraps=Request)
def test_post_request_executed(RequestMock, starwars_data):
    query = '{hero{name}}'
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
    assert json.loads(response.content.decode('utf-8')) == {
        'data': {'hero': {'name': 'R2-D2'}},
    }
    RequestMock.assert_called_once_with(
        document=query,
        variables=None,
        operation_name=None,
        schema=schema,
    )


@mock.patch('django_graph_api.views.Request', wraps=Request)
def test_variables_sent_in_post(RequestMock, starwars_data):
    query = '''
        query EpisodeName($number: Int) {
            episode (number: $number) {
                name
            }
        }
    '''
    client = Client()
    response = client.post(
        '/graphql',
        json.dumps({
            'query': query,
            'variables': {
                'number': 4
            },
        }),
        content_type='application/json',
        HTTP_ACCEPT='application/json',
    )
    assert isinstance(response, JsonResponse)
    assert response.status_code == 200
    assert json.loads(response.content.decode('utf-8')) == {
        'data': {'episode': {'name': 'A New Hope'}},
    }
    RequestMock.assert_called_once_with(
        document=query,
        variables={'number': 4},
        operation_name=None,
        schema=schema,
    )


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


def test_post_empty_string():
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


def test_post_empty_query():
    client = Client()
    response = client.post(
        '/graphql',
        '{"query": ""}',
        content_type='application/json',
        HTTP_ACCEPT='application/json',
    )
    assert isinstance(response, JsonResponse)
    assert response.status_code == 200
    response_json = json.loads(response.content.decode('utf-8'))
    print(response_json)
    assert response_json['errors'][0]['message'] == 'Must provide query string.'


@modify_settings(MIDDLEWARE={'remove': 'django.middleware.csrf.CsrfViewMiddleware'})
@mock.patch('django_graph_api.views.Request')
def test_post__csrf_required(RequestMock, starwars_data):
    query = '{hero{name}}'
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
    RequestMock.execute.assert_not_called()
