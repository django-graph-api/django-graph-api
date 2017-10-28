from django.db import models


class Episode(models.Model):
    name = models.CharField(max_length=255)
    number = models.IntegerField()

    def __str__(self):
        return '{}: {}'.format(self.number, self.name)

    class Meta(object):
        ordering = ['number']


class Starship(models.Model):
    name = models.CharField(max_length=255)
    length = models.FloatField(default=0)


class Character(models.Model):
    name = models.CharField(max_length=255)
    friends = models.ManyToManyField('self', blank=True)
    appears_in = models.ManyToManyField(
        Episode,
        blank=True,
        related_name='characters',
    )

    def __str__(self):
        return self.name

    class Meta(object):
        ordering = ['pk']


class Human(Character):
    starships = models.ManyToManyField(Starship)
    total_credits = models.PositiveSmallIntegerField(default=0)


class Droid(Character):
    primary_function = models.CharField(max_length=255)
