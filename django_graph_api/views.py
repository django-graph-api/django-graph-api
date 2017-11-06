from traceback import format_exc
import json

from django.conf import settings
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
    """
    Django view handles Graph API queries.

    ``GET`` returns the HTML for the GraphiQL API explorer.

    ``POST`` accepts a body in the form of ``{'query': query, 'variables': null}`` and returns a JSON response with
    either a "data" or "error" object.
    """
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
            error_data = {
                'error': str(e),
            }

            if settings.DEBUG:
                error_data['traceback'] = format_exc().split('\n')

            return JsonResponse(error_data)

    def get_request_data(self):
        """
        Takes an incoming request and parses it into a dictionary containing
        query and variables. For now we only support json dictionaries in
        the style of GraphiQL, i.e. {'query': query, 'variables': null}
        """
        body = self.request.body.decode('utf-8')
        return json.loads(body)
