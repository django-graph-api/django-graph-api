from django.http import JsonResponse


from django.template.response import TemplateResponse
from django.views.generic import View


class GraphQLView(View):
    graphiql_version = '0.11.3'
    template_name = 'django_graph_api/graphiql.html'

    def html_requested(self):
        """
        This naive implementation just checks whether html is one
        of the accepted formats. This is not correct handling of
        the Accept header; however, it should work for most cases.
        """
        if 'text/html' in self.request.META.get('HTTP_ACCEPT', ''):
            return True

        return False

    def get(self, request, *args, **kwargs):
        if self.html_requested():
            return TemplateResponse(
                request=self.request,
                template=[self.template_name],
                context={
                    'graphiql_version': self.graphiql_version,
                },
            )

        return JsonResponse(self.execute())

    def execute(self):
        return {}
