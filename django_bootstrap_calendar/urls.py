# -*- coding: utf-8 -*-
__author__ = "sandlbn"

from django.urls import path
from .views import CalendarJsonListView, CalendarView

urlpatterns = [
    path("json/", CalendarJsonListView.as_view(), name="calendar_json"),
    path("", CalendarView.as_view(), name="calendar"),
]
