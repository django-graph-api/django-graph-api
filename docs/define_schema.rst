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

Create an Object node for each of the models
and define their fields.
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

You can also override a Django model's field in the Graph API
or create an additional field.
::

    class Episode(Object):
        ...
        long_name = CharField()

    def get_long_name(self):
        return 'Episode {}: {}'.format(
            int_to_roman_numeral(self.number),
            self.name)

Adding edges - Relationships
----------------------------

Define relationship fields between the objects.

Many-to-many, 1-to-many relationships
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If querying on the relationship should return a **list**,
use ``ManyRelatedField``.
::

    from django_graph_api import ManyRelatedField

    class Character(Object):
        ...
        friends = ManyRelatedField('self')
        appears_in = ManyRelatedField(Episode)


1-to-1, many-to-1 relationships
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If querying on the relationship should return an **object**,
use ``RelatedField``.
::

    from django_graph_api import RelatedField
    from .models import Episode as EpisodeModel

    class Episode(Object):
        ...
        previous = RelatedField('self')
        next = RelatedField('self')

        get_previous(self):
            return EpisodeModel.objects.filter(number=self.number-1).first()

        get_next(self):
            return EpisodeModel.objects.filter(number=self.number+1).first()

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
        episodes = ManyRelatedField(Episode)

        def get_hero(self):
            return CharacterModel.objects.get(name='R2-D2')

        def get_episodes(self):
            return EpisodeModel.objects.all()

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
