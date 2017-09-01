from django.conf.urls import url

from django_graph_api.views import GraphQLView
from .starwars.schema import schema


urlpatterns = [
    url(r'^graphql$', GraphQLView.as_view(schema=schema)),
]
