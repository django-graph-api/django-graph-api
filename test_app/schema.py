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
    Episode as EpisodeModel,
)


schema = Schema()


class Episode(Object):
    name = CharField()
    number = IntegerField()
    characters = ManyRelatedField(lambda: Character)

    next = RelatedField('self')

    def get_next(self):
        return EpisodeModel.objects.filter(number=self.data.number + 1).first()


class Character(Object):
    name = CharField()
    friends = ManyRelatedField('self')
    best_friend = RelatedField('self')
    appears_in = ManyRelatedField(Episode)

    def get_best_friend(self):
        return self.data.friends.order_by('pk').first()


@schema.register_query_root
class QueryRoot(Object):
    hero = RelatedField(Character)
    episodes = ManyRelatedField(Episode)

    def get_hero(self):
        return CharacterModel.objects.get(name='R2-D2')

    def get_episodes(self):
        return EpisodeModel.objects.order_by('number')
