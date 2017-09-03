import json

from django.http import JsonResponse
from django.template.response import TemplateResponse
from django.views.generic import View


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
        request_data = self.get_request_data()
        response_data = self.schema.execute(request_data['query'])
        return JsonResponse(response_data)

    def get_request_data(self):
        """
        Takes an incoming request and parses it into a dictionary containing
        query and variables. For now we only support json dictionaries in
        the style of GraphiQL, i.e. {'query': query, 'variables': null}
        """
        body = self.request.body.decode('utf-8')
        return json.loads(body)
