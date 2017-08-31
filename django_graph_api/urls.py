from django.conf.urls import url

from django_graph_api.views import GraphQLView


urlpatterns = [
    url(r'^$', GraphQLView.as_view()),
]
