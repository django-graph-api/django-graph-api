Create a full schema
=======================
While that setup was certainly quick and easy, it is not very useful yet. Next you will want to create a graph-like schema that maps to your business logic so you can query against it.

Using the Star Wars example from the GraphQL documentation_, let's assume we have a Django app with the following model structure:
Characters are friends with other Characters and appear in Episodes.

Adding nodes
------------

Create a node for each of your models
::

    from django_graph_api.graphql.types import (
        Object,
        CharField,
        IntegerField,
    )

    class Episode(Object):
        name = CharField()
        number = IntegerField()

    class Character(Object):
        name = CharField()

Adding edges
------------
Create connections between your models
::

    from django_graph_api.graphql.types import ManyRelatedField

    class Character(Object):
        name = CharField()
        friends = ManyRelatedField('self')
        appears_in = ManyRelatedField(Episode)


Defining query roots
--------------------

By defining query roots, you can control how the user can access the schema.
::

    from django_graph_api.types import RelatedField
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

You should now be able to create more complicated queries and make use of GraphQL's nested object feature.
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
