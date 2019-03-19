from django.db import models
from django.contrib.auth.models import User
import datetime


import hashlib

class Refill(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    prescription = models.CharField(max_length=60, help_text="RX Name")
    nickname = models.CharField(max_length=60, null=True, blank=True, help_text="Optional: Name that will display on calendar event instead of RX Name", verbose_name='Medicine Nickname')
    pharmacy = models.CharField(max_length=240, null=True, blank=True, help_text="Name and Location", verbose_name="Pharmacy for Refill")
    refill_date = models.DateField(default=datetime.date.today, help_text="Next date to refill med")

        
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

