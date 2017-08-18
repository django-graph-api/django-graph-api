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


def test_simple_query_one_level():
    document = '''
    {
        hello
    }
    '''
    assert schema.execute(document) == {
        'data': {
            'hello': 'world',
        },
    }


def test_simple_query_two_levels():
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


def test_simple_query_three_levels():
    document = '''
    {
        yavin {
            hero {
                name
            }
        }
        endor {
            hero {
                name
            }
    }
    '''
    assert schema.execute(document) == {
        'data': {
            'yavin': {
                'hero': {
                    'name': 'Luke',
                },
            },
            'endor': {
                'hero': {
                    'name': 'Han',
                },
            },
        }
    }
