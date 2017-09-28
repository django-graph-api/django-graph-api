Defining nodes
===========================================

Define some nodes
::
    from django_graph_api.graphql.types import (
        Object,
        CharField,
        IntegerField,
        ManyRelatedField,
    )

    class Episode(Object):
        name = CharField()
        number = IntegerField()

    class Character(Object):
        name = CharField()
        friends = ManyRelatedField('self')
        appears_in = ManyRelatedField(Episode)

Create at least one query root
::
    from django_graph_api.types import RelatedField
    from .models import (
        Character as CharacterModel,
    )

    @schema.register_query_root
    class QueryRoot(Object):
        hero = RelatedField(Character)

        def get_hero(self):
            return CharacterModel.objects.get(name='R2-D2')

