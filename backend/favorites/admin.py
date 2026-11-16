from django.contrib import admin

from .models import Favorite, ReviewList

admin.site.register(Favorite)
admin.site.register(ReviewList)
