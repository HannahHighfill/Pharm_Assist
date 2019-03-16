from django.db import models
from django.contrib.auth.models import User


import hashlib

class Tweet(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    text = models.CharField(max_length=160)

    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    image = models.FileField(upload_to='tweet_images/', null=True, blank=True)

    liked = models.ManyToManyField(
        User,
        related_name="liked_tweets",
    )

    def get_gravatar(self):
        # This is the example code found online for Gravatar, which will
        # randomly generate avatars based on email (we'll use username in this
        # case).
        email = self.username
        encoded = hashlib.md5(email.encode('utf8')).hexdigest()
        gravatar_url = "http://www.gravatar.com/avatar/%s?d=identicon" % encoded
        return gravatar_url

    def __str__(self):
        return self.user.name + ' said ' + self.text
        
class RefillEvent(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    summary = models.CharField(max_length=160)
    location = models.CharField(max_length=160)
    description = models.TextField()
    startdatetime = models.DateTimeField()
    timezone = models.CharField(max_length=160, default='America/Los_Angeles')
    enddatetime = models.DateTimeField()
    postedtocalendar = models.BooleanField(default=False)
#    recurrence = 'RRULE:FREQ=DAILY;COUNT=2'
#    reminder = models.BooleanField()
# This will create a table in sqlite. make a form from it. use the form to populate an event variable. the calendar views adds that event to the calendar

