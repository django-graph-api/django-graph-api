import json

from django.http import JsonResponse
from django.template.response import TemplateResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import (
    csrf_protect,
    ensure_csrf_cookie,
)
from django.views.generic import View

from django_graph_api.graphql.request import Request


class GraphQLView(View):
    """
    Django view handles Graph API queries.

    ``GET`` returns the HTML for the GraphiQL API explorer.

    ``POST`` accepts a JSON body in the form of::

        {
            "query": <query>,
            "variables": <variables>
        }

    and returns a JSON response with a "data" and/or "error" object.
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
        # Python 2 json library raises ValueError; Python 3 raises more specific error.
        JSONDecodeError = getattr(json, 'JSONDecodeError', ValueError)

        try:
            request_data = self.get_request_data()
            graphql_request = Request(
                document=request_data['query'],
                variables=request_data.get('variables'),
                operation_name=request_data.get('operationName'),
                schema=self.schema
            )
        except (KeyError, JSONDecodeError):
            return JsonResponse({
                'errors': [
                    {'message': 'Data must be json with a "query" key and optional "variables" key'},
                ],
            })

        graphql_request.validate()
        data = None
        errors = graphql_request.errors
        if not errors:
            data, errors = graphql_request.execute()

        response = {}
        if data:
            response['data'] = data

        if errors:
            response['errors'] = [error.serialize() for error in errors]
        return JsonResponse(response)

    def get_request_data(self):
        """
        Takes an incoming request and parses it into a dictionary containing
        query and variables. For now we only support json dictionaries in
        the style of GraphiQL, i.e. {"query": query, "variables": null}
        """
        body = self.request.body.decode('utf-8')
        return json.loads(body)
