from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
import pytz


import hashlib

REPEATS_CHOICES = (
        ('WEEKLY', 'weeks'),
        ('MONTHLY', 'months'),
    )



TIMEZONE_CHOICES = (
        ('America/Los_Angeles', 'Pacific'),
        ('America/Denver', 'Mountain'),
        ('America/Chicago', 'Central'),
        ('America/New_York', 'Eastern'),
    )

class Refill(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    prescription = models.CharField(max_length=60, help_text="Medicine Name")
    nickname = models.CharField(max_length=60, null=True, blank=True, help_text="Optional: Name that will display on calendar event instead of Medicine Name", verbose_name='Medicine Nickname')
    pharmacy = models.CharField(max_length=240, null=True, blank=True, help_text="Name and Location", verbose_name="Pharmacy for Refill")
    refill_date = models.DateField(default=datetime.date.today, help_text="Next date to refill med")
    refill_time = models.TimeField(default=datetime.time(12, 00, 00), null=True, blank=True)
    refill_time = models.TimeField(default=datetime.time(12, 00, 00), null=True, blank=True)
    all_day = models.BooleanField(default=False, blank=True)
    often = models.IntegerField(default=1, validators=[MinValueValidator(0), MaxValueValidator(20)], null=True, blank=True, verbose_name="Repeates Every")
    repeats = models.CharField(max_length=9, choices= REPEATS_CHOICES, null=True, blank=True, verbose_name="")


#Jamie thinks we will end up deleting this
class RefillEvent(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    
    # Added Refill form fields from views.py: 'Prescription', 'Nickname', 'Pharmacy', 'Date'
    prescription = models.CharField(max_length=160)
    nickname = models.CharField(max_length=160)
    pharmacy = models.TextField()
    number = models.CharField(max_length=160)
    timezone = models.CharField(max_length=160, default='America/Los_Angeles')
    postedtocalendar = models.BooleanField(default=False)
#    recurrence = 'RRULE:FREQ=DAILY;COUNT=2'
#    reminder = models.BooleanField()
# This will create a table in sqlite. make a form from it. use the form to populate an event variable. the calendar views adds that event to the calendar

