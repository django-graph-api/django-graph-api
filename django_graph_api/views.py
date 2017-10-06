import json

from django.http import JsonResponse
from django.template.response import TemplateResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import (
    csrf_protect,
    ensure_csrf_cookie,
)
from django.views.generic import View


@method_decorator([ensure_csrf_cookie, csrf_protect], name='dispatch')
class GraphQLView(View):
    graphiql_version = '0.11.3'
    graphql_url = '/graphql'
    template_name = 'django_graph_api/graphiql.html'
    schema = None

    def get(self, request, *args, **kwargs):
        return TemplateResponse(
            request=self.request,
            template=[self.template_name],
            context={
                'graphiql_version': self.graphiql_version,
                'graphql_url': self.graphql_url,
            },
        )

    def post(self, request, *args, **kwargs):
        try:
            request_data = self.get_request_data()
            response_data = self.schema.execute(request_data['query'])
            return JsonResponse(response_data)
        except Exception as e:
            if isinstance(e, KeyError) and str(e) == "'__schema'":
                return JsonResponse({
                    'error': 'This version of django-graph-api does not support introspection',
                })
            return JsonResponse({'error': str(e)})

    def get_request_data(self):
        """
        Takes an incoming request and parses it into a dictionary containing
        query and variables. For now we only support json dictionaries in
        the style of GraphiQL, i.e. {'query': query, 'variables': null}
        """
        body = self.request.body.decode('utf-8')
        return json.loads(body)
