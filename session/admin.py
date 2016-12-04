from django.contrib import admin

from session.models import Session, Location

admin.site.register(Location)
admin.site.register(Session)

