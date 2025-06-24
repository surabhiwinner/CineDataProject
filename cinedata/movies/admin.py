from django.contrib import admin


from . import models
# Register your models here.

admin.site.register(models.Movies)

admin.site.register(models.Artist)

admin.site.register(models.Production)

admin.site.register(models.Genre)

admin.site.register(models.Rating)