Defining the schema
===================
GraphQL requires a graph-like schema to query against.
The nodes and edges of the graph will be
the objects and relationships in your API.

Using the Star Wars example from the GraphQL documentation_,
let's assume we have a Django app with the following model structure:

- Characters appear in Episodes.
- Characters are friends with other Characters.

Adding nodes - Objects
----------------------

Create an Object node for each of the models:
::

    from django_graph_api import (
        Object,
    )

    class Episode(Object):
        ...

    class Character(Object):
        ...

Add scalar fields to each of the nodes:
::

    from django_graph_api import (
        Object,
        CharField,
        IntegerField,
    )

    class Episode(Object):
        name = CharField()
        number = IntegerField()

    class Character(Object):
        name = CharField()

You can define any field on the node (Object)
that is also a **field** or **property** of the model
that it represents.
You can also define custom logic to get a field's value by adding a ``get_<field_name>`` method to the object.
The current model instance will be available as ``self.data``.

Arguments can be defined for fields by passing in ``<argname>=<graphql type instance>``.
The value passed in a query will be available as a keyword argument to the field value method if there is one.
::
    from django_graph_api.graphql.types import Boolean

    class Character(Object):
        name = CharField(upper=Boolean())

        def get_name(self, upper=False):
            name = '{} {}'.format(
                self.data.first_name,
                self.data.last_name,
            )
            if upper:
                return name.upper()
            return name

You may also define descriptions for individual fields in the same way as the other keyword arguments.
::
    class Character(Object):
        name = CharField(description="The name of a character.")

The difference here is that if you're inspecting the schema in the GraphiQL front-end, the description for the field will appear under the name of the field.
The query itself will not change in any other way.

Scalar field types
^^^^^^^^^^^^^^^^^^
For scalar types,
the type of the field determines how it will be returned by the API.

For example, if a model's field is stored as an ``IntegerField`` on the Django model
and defined as a ``CharField`` in the graph API,
the model value will be coerced from an ``int`` to a ``str`` type
when it is resolved.

Supported scalar types can be found in the `API documentation`_ and `feature list`_.

.. _API documentation: api.html#scalar-field-types
.. _feature list: features.html#types


Adding edges - Relationships
----------------------------

In order to traverse the nodes in your graph schema
you need to define relationships between them.

This is done by adding related fields to your Object nodes.
These `non-scalar fields`_ will return
other objects or a list of objects.

- If the field should return an **object**, use ``RelatedField``
- If the field should return a **list** of objects, use ``ManyRelatedField``

When defining the object type of the related field, you can use:

- The class of the object, e.g. ``appears_in = ManyRelatedField(Episode)``
- A callable that returns the class of the object, e.g. ``characters = ManyRelatedField(lambda: Character)``
- 'self', when you are referencing the current class, e.g. ``mother = RelatedField('self')``

You can define any related field on the node (Object)
that is also a **field** or **property** of the model
that returns another model, list of models, or model manager.
You can also define custom logic by adding a ``get_<field_name>`` method to the object.
The current model instance will be available as ``self.data``.

Examples
^^^^^^^^

Many-to-many relationship
::

    from django_graph_api import (
        ManyRelatedField,
    )

    class Episode(Object):
        characters = ManyRelatedField(lambda: Character)

    class Character(Object):
        appears_in = ManyRelatedField(Episode)

Many-to-one relationship
::

    from django_graph_api import (
        ManyRelatedField,
        RelatedField,
    )

    class Character(Object):
        mother = RelatedField('self')
        children = ManyRelatedField('self')

One-to-one relationship
::

    from django_graph_api import (
        RelatedField,
    )

    from .models import {
        Episode as EpisodeModel
    }

    class Episode(Object):
        next = RelatedField('self')
        previous = RelatedField('self')

        def get_next(self):
            return EpisodeModel.objects.filter(number=self.data.number + 1).first()

        def get_previous(self):
            return EpisodeModel.objects.filter(number=self.data.number - 1).first()

.. _non-scalar fields: api.html#non-scalar-field-types


Defining query roots
--------------------

By defining query roots, you can control how the user can access the schema.
::

    from django_graph_api import RelatedField
    from .models import Character as CharacterModel
    from .models import Episode as EpisodeModel

    @schema.register_query_root
    class QueryRoot(Object):
        hero = RelatedField(Character)

        def get_hero(self):
            return CharacterModel.objects.get(name='R2-D2')

Sample queries
--------------

You should now be able to create more complicated queries
and make use of GraphQL's nested objects feature.
::

    {
        hero {
            friends {
                name
            }
            appears_in {
                name
                number
            }
        }
    }

.. _documentation: http://graphql.org/learn/
