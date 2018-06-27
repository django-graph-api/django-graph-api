API reference
=============

Schema
------
.. autoclass:: django_graph_api.Schema
   :members: __init__

Request
-------
.. autoclass:: django_graph_api.Request
   :members: execute, validate

Types
-----

Non-scalar field types
^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: django_graph_api.Object
.. autoclass:: django_graph_api.RelatedField
.. autoclass:: django_graph_api.ManyRelatedField

Scalar field types
^^^^^^^^^^^^^^^^^^
.. autoclass:: django_graph_api.BooleanField
.. autoclass:: django_graph_api.CharField
.. autoclass:: django_graph_api.IdField
.. autoclass:: django_graph_api.IntegerField
.. autoclass:: django_graph_api.FloatField

Views
-----
.. autoclass:: django_graph_api.GraphQLView
