# -*- coding: utf-8 -*-
__author__ = "sandlbn"

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from .utils import datetime_to_timestamp

class CalendarEvent(models.Model):
    """
    Calendar Events
    """

    CSS_CLASS_CHOICES = (
        ("", _("Normal")),
        ("event-warning", _("Warning")),
        ("event-info", _("Info")),
        ("event-success", _("Success")),
        ("event-inverse", _("Inverse")),
        ("event-special", _("Special")),
        ("event-important", _("Important")),
    )
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    url = models.URLField(verbose_name=_("URL"), null=True, blank=True)
    css_class = models.CharField(
        blank=True,
        max_length=20,
        verbose_name=_("CSS Class"),
        choices=CSS_CLASS_CHOICES,
    )
    exclusive = models.BooleanField(verbose_name=_("Exclusive to Use (no double booking)"),default=False)
    start = models.DateTimeField(verbose_name=_("Start Date"))
    end = models.DateTimeField(verbose_name=_("End Date"), null=True, blank=True)

    def clean(self):
        if not self.exclusive: return True #nothing to check

        overlaps_with_start = CalendarEvent.objects.filter(start__lt=self.start, end__gt=self.start)
        overlaps_with_end = CalendarEvent.objects.filter(start__lt=self.end, end__gt=self.end)

        if overlaps_with_start.exists() or overlaps_with_end.exists():
            raise ValidationError("Cannot double-book the model")
        return True

    def save(self, *args, **kwargs):
        self.clean()  # Call the clean method before saving
        super().save(*args, **kwargs)

    @property
    def start_timestamp(self):
        """
        Return start date as timestamp
        """
        return datetime_to_timestamp(self.start)

    @property
    def end_timestamp(self):
        """
        Return end date as timestamp
        """
        return datetime_to_timestamp(self.end)

    def __str__(self):
        return self.title
