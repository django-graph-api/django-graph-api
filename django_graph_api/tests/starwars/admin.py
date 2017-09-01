from django.contrib import admin

from .models import (
    Character,
    Droid,
    Episode,
    Human,
    Starship,
)

admin.site.register(Character)
admin.site.register(Droid)
admin.site.register(Episode)
admin.site.register(Human)
admin.site.register(Starship)
