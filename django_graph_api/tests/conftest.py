import pytest

from test_app.models import (
    Droid,
    Episode,
    Human,
)


@pytest.fixture
def starwars_data(transactional_db):
    luke, _ = Human.objects.get_or_create(
        id=1000,
        name='Luke Skywalker',
    )
    darth_vader, _ = Human.objects.get_or_create(
        id=1001,
        name='Darth Vader',
    )
    han, _ = Human.objects.get_or_create(
        id=1002,
        name='Han Solo',
    )
    leia, _ = Human.objects.get_or_create(
        id=1003,
        name='Leia Organa',
    )
    c3po, _ = Droid.objects.get_or_create(
        id=2000,
        name='C-3PO',
        primary_function='Protocol',
    )
    r2d2, _ = Droid.objects.get_or_create(
        id=2001,
        name='R2-D2',
        primary_function='Astromech',
    )

    for friend in (han, leia, c3po, r2d2):
        luke.friends.add(friend)
    han.friends.add(leia)
    han.friends.add(r2d2)
    leia.friends.add(c3po)
    leia.friends.add(r2d2)
    c3po.friends.add(r2d2)

    a_new_hope, _ = Episode.objects.get_or_create(
        id=1,
        name='A New Hope',
        number=4
    )

    empire_strikes_back, _ = Episode.objects.get_or_create(
        id=2,
        name='The Empire Strikes Back',
        number=5
    )

    for character in (luke, han, leia, c3po, r2d2, darth_vader):
        a_new_hope.characters.add(character)
        empire_strikes_back.characters.add(character)
