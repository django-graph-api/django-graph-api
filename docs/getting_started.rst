Getting started
============================================

Install
+++++++

Download or clone the repo_ and navigate to the directory.
::
    pip install -e .

*Note:* once the project is up on PyPI you can run ``pip install django-graph-api``

Create a basic schema
+++++++++++++++++++++

GraphQL APIs require a graph-like schema and at least one entry-point (query root) to the graph.

Here is an example of a schema with a single node.
::
    from django_graph_api.graphql.schema import Schema
    from django_graph_api.graphql.types import CharField

    schema = Schema()

    @schema.register_query_root
    class QueryRoot(Object):
        hello = CharField()

        def get_hello(self):
            return 'World'

Set up a url to access the schema
+++++++++++++++++++++++++++++++++

GraphQL APIs use a single url endpoint to access the schema.
::
    from django_graph_api.views import GraphQLView

    urlpatterns = [
        ...
        url(r'^graphql$', GraphQLView.as_view(schema=schema)),
    ]

This url will act as both the GraphQL endpoint to send AJAX requests too, and be the url that allows you to access the GraphiQL (graphical) application.

.. _repo: https://github.com/melinath/django-graph-api
