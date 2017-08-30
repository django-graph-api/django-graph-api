from django.db import models


class Episode(models.Model):
    name = models.CharField(max_length=255)
    number = models.IntegerField(max_length=1)


class Starship(models.Model):
    name = models.CharField(max_length=255)
    length = models.FloatField(default=0)


class Character(models.Model):
    name = models.CharField(max_length=255)
    friends = models.ManyToManyField('self')
    appears_in = models.ManyToManyField(Episode, related_name='characters')


class Human(Character):
    starships = models.ManyToManyField(Starship)
    total_credits = models.PositiveSmallIntegerField(default=0)


class Droid(Character):
    primary_function = models.CharField(max_length=255)
