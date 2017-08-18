from django_graph_api.graphql.schema import schema
from django_graph_api.graphql.types import (
    Object,
    CharField,
    ObjectField,
)


data = {
    'heroes': {
        '200': {
            'name': 'R2-D2',
        }
    }
}


@schema.register_type
class Hero(Object):
    name = CharField()


@schema.register_query_root
@schema.register_type
class QueryRoot(Object):
    hero = ObjectField(Hero)

    def get_hero(self):
        return data['heroes']['200']


def test_simple_query():
    document = '''
    {
        hero {
            name
        }
    }
    '''
    assert schema.execute(document) == {
        'data': {
            'hero': {
                'name': 'R2-D2',
            },
        }
    }
