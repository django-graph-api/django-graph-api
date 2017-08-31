from django.http import JsonResponse
from django.template.response import TemplateResponse
from django.views.generic import View

from django_graph_api.graphql.schema import schema


class GraphQLView(View):
    graphiql_version = '0.11.3'
    template_name = 'django_graph_api/graphiql.html'

    def get(self, request, *args, **kwargs):
        return TemplateResponse(
            request=self.request,
            template=[self.template_name],
            context={
                'graphiql_version': self.graphiql_version,
            },
        )

    def post(self, request, *args, **kwargs):
        document = request.body.decode()
        data = schema.execute(document)
        return JsonResponse(data)
