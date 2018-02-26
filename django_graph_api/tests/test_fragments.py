from django_graph_api.graphql.request import Request

from test_app.schema import QueryRoot


def test_fragments(starwars_data):
    document = '''
    {
        hero {
            ...heroFragment
        }
        episodes {
            ...episodeFragment
        }
    }

    fragment heroFragment on Character {
        id
        name
    }

    fragment episodeFragment on Episode {
        name
        number
    }
    '''
    request = Request(
        document=document,
        query_root_class=QueryRoot,
    )
    data, errors = request.execute()
    assert data == {
        'episodes': [
            {
                'name': 'A New Hope',
                'number': 4,
            },
            {
                'name': 'The Empire Strikes Back',
                'number': 5,
            },
        ],
        'hero': {
            'name': 'R2-D2',
            'id': 2001,
        },
    }
    assert errors == []


def test_fragments__nested(starwars_data):
    document = '''
    {
        hero {
            ...heroIdFragment
        }
    }

    fragment heroIdFragment on Character {
        id
        ...heroNameFragment
    }

    fragment heroNameFragment on Character {
        name
    }
    '''
    request = Request(
        document=document,
        query_root_class=QueryRoot,
    )
    data, errors = request.execute()
    assert data == {
        'hero': {
            'name': 'R2-D2',
            'id': 2001,
        },
    }
    assert errors == []


def test_fragments__recursive(starwars_data):
    document = '''
    {
        hero {
            ...heroIdFragment
        }
    }

    fragment heroIdFragment on Character {
        id
        ...heroNameFragment
    }

    fragment heroNameFragment on Character {
        name
        ...heroIdFragment
    }
    '''
    request = Request(
        document=document,
        query_root_class=QueryRoot,
    )
    data, errors = request.execute()
    assert data == {
        'hero': {
            'name': 'R2-D2',
            'id': 2001,
        },
    }
    assert errors == []


def test_fragments__inline(starwars_data):
    document = '''
    {
        hero {
            ... on Character {
                id
                name
            }
        }
        episodes {
            ... on Episode {
                name
                number
            }
        }
    }
    '''
    request = Request(
        document=document,
        query_root_class=QueryRoot,
    )
    data, errors = request.execute()
    assert data == {
        'episodes': [
            {
                'name': 'A New Hope',
                'number': 4,
            },
            {
                'name': 'The Empire Strikes Back',
                'number': 5,
            },
        ],
        'hero': {
            'name': 'R2-D2',
            'id': 2001,
        },
    }
    assert errors == []
