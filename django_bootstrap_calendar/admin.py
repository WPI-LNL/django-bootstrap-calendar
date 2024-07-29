from django.contrib import admin
from django.conf import settings

from .models import CalendarEvent

if getattr(settings,'REGISTER_CALENDAR_EVENTS_MODEL',True):
    admin.site.register(CalendarEvent)
