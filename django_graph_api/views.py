import json

from django.http import JsonResponse
from django.template.response import TemplateResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import (
    csrf_protect,
    ensure_csrf_cookie,
)
from django.views.generic import View

from django_graph_api.graphql.utils import (
    format_error,
    GraphQLError
)


class GraphQLView(View):
    """
    Django view handles Graph API queries.

    ``GET`` returns the HTML for the GraphiQL API explorer.

    ``POST`` accepts a body in the form of ``{'query': query, 'variables': variables}`` and returns a JSON response with
    either a "data" or "error" object.
    """
    graphiql_version = '0.11.11'
    graphql_url = '/graphql'
    template_name = 'django_graph_api/graphiql.html'
    schema = None

    @method_decorator(ensure_csrf_cookie)
    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super(GraphQLView, self).dispatch(*args, **kwargs)

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
            query = request_data['query']
            variables = request_data.get('variables')
        except Exception:
            error = GraphQLError('Data must be json with a "query" key and optional "variables" key')
            return JsonResponse({'errors': [(format_error(error))]})

        try:
            response_data = self.schema.execute(query, variables)
            return JsonResponse(response_data)
        except Exception as e:
            error = GraphQLError('Execution error: {}'.format(str(e)))
            return JsonResponse({'errors': [(format_error(error))]})

    def get_request_data(self):
        """
        Takes an incoming request and parses it into a dictionary containing
        query and variables. For now we only support json dictionaries in
        the style of GraphiQL, i.e. {'query': query, 'variables': null}
        """
        body = self.request.body.decode('utf-8')
        return json.loads(body)
