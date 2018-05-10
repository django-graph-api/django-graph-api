from django.conf.urls import url
from django.contrib import admin

from django_graph_api.views import GraphQLView
from test_app.schema import schema


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^graphql$', GraphQLView.as_view(schema=schema)),
]
