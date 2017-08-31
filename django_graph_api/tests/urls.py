from django.conf.urls import include, url

urlpatterns = [
    url(r'^graphql/', include('django_graph_api.urls')),
]
