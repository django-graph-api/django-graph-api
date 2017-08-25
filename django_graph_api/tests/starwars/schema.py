from django_graph_api.graphql.schema import Schema
from django_graph_api.graphql.types import (
    Object,
    CharField,
    RelatedField,
    ManyRelatedField,
)

from .models import (
    Character as CharacterModel,
)


schema = Schema()


@schema.register_type
class Character(Object):
    name = CharField()
    friends = ManyRelatedField('self')


@schema.register_query_root
@schema.register_type
class QueryRoot(Object):
    hero = RelatedField(Character)

    def get_hero(self):
        return CharacterModel.objects.get(name='R2-D2')
