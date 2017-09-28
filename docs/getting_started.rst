Getting started
============================================

1. ``pip install django-graph-api``

2. Add ``'django_graph_api'`` to your installed apps

3. Create a schema
::
    from django_graph_api.graphql.schema import Schema
    schema = Schema()

4. Set up a url endpoint to access the schema
::
    from django_graph_api.views import GraphQLView
    from .starwars.schema import schema

    urlpatterns = [
        ...
        url(r'^graphql$', GraphQLView.as_view(schema=schema)),
    ]

Now, you should be able to got to the url and view the Graphiql app. You won't be able to query on anything yet though because you haven't identified any nodes in your schema.
