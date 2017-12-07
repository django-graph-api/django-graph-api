import pytest

from test_app.models import (
    Droid,
    Episode,
    Human,
)


@pytest.fixture
def starwars_data(transactional_db):
    luke = Human.objects.create(
        id=1000,
        name='Luke Skywalker',
    )
    darth_vader = Human.objects.create(
        id=1001,
        name='Darth Vader',
    )
    han = Human.objects.create(
        id=1002,
        name='Han Solo',
    )
    leia = Human.objects.create(
        id=1003,
        name='Leia Organa',
    )
    c3po = Droid.objects.create(
        id=2000,
        name='C-3PO',
        primary_function='Protocol',
    )
    r2d2 = Droid.objects.create(
        id=2001,
        name='R2-D2',
        primary_function='Astromech',
    )

    luke.friends = [han, leia, c3po, r2d2]
    han.friends.add(leia)
    han.friends.add(r2d2)
    leia.friends.add(c3po)
    leia.friends.add(r2d2)
    c3po.friends.add(r2d2)

    a_new_hope = Episode.objects.create(
        id=1,
        name='A New Hope',
        number=4
    )

    a_new_hope.characters = [luke, han, leia, c3po, r2d2, darth_vader]

    empire_strikes_back = Episode.objects.create(
        id=2,
        name='The Empire Strikes Back',
        number=5
    )

    empire_strikes_back.characters = [luke, han, leia, c3po, r2d2, darth_vader]
