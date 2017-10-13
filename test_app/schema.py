from django_graph_api.graphql.schema import Schema
from django_graph_api.graphql.types import (
    Object,
    CharField,
    IntegerField,
    RelatedField,
    ManyRelatedField,
)

from .models import (
    Character as CharacterModel,
)


schema = Schema()


class Episode(Object):
    name = CharField()
    number = IntegerField()


class Character(Object):
    name = CharField()
    friends = ManyRelatedField('self')
    appears_in = ManyRelatedField(Episode)


@schema.register_query_root
class QueryRoot(Object):
    hero = RelatedField(Character)

    def get_hero(self):
        return CharacterModel.objects.get(name='R2-D2')
