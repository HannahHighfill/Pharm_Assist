from __future__ import print_function
import datetime
from datetime import timedelta
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request # All from google api example

from django.shortcuts import render, redirect
from django import forms
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import logout as auth_logout


from .models import Tweet

SCOPES = ['https://www.googleapis.com/auth/calendar.events']


class NewUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password', 'email']


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['text', 'image']


def homepage(request):
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request
        form = NewUserForm(request.POST)

        if form.is_valid():
            # Create a new user object using the ModelForm's built-in .save()
            # giving it from the cleaned_data form.
            user = form.save()

            # As soon as our new user is created, we make this user be
            # instantly "logged in".
            auth.login(request, user)
            return redirect('/')

    else:
        # if a GET we'll create a blank form
        form = NewUserForm()

    context = {
        'form': form,
    }
    return render(request, 'pages/homepage.html', context)

def login(request):
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    context={
    }
    return render(request, 'pages/login.html', context)

def logout(request):
    auth_logout(request)
    return redirect(request.META.get('HTTP_REFERER', '/'))
    
def calendar(request):
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

            service = build('calendar', 'v3', credentials=creds)

            # Call the Calendar API
            now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
            event = {
  'summary': 'Google I/O 2015',
  'location': '800 Howard St., San Francisco, CA 94103',
  'description': 'A chance to hear more about Google\'s developer products.',
  'start': {
    'dateTime': '2019-03-15T09:00:00-07:00',
    'timeZone': 'America/Los_Angeles',
  },
  'end': {
    'dateTime': '2019-03-15T17:00:00-07:00',
    'timeZone': 'America/Los_Angeles',
  },
  'recurrence': [
    'RRULE:FREQ=DAILY;COUNT=2'
  ],
  'attendees': [
    {'email': 'lpage@example.com'},
    {'email': 'sbrin@example.com'},
  ],
  'reminders': {
    'useDefault': False,
    'overrides': [
      {'method': 'email', 'minutes': 24 * 60},
      {'method': 'popup', 'minutes': 10},
    ],
  },
            }

            event = service.events().insert(calendarId='primary', body=event).execute()
            print ('Event created: %s' % (event.get('htmlLink')))
            print('Getting the upcoming 10 events')
            events_result = service.events().list(calendarId='primary', timeMin=now,
                                                maxResults=10, singleEvents=True,
                                                orderBy='startTime').execute()
            events = events_result.get('items', [])
            #print(events) --> list with dictionaries
            if not events:
                print('No upcoming events found.')
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                print(start, event['summary'])
                
            context={
                'username':request.user.username 
            }
            return render(request, 'pages/calendar.html', context)

def view_all_tweets(request):
    tweets = Tweet.objects.order_by('-created')
    context = {
        'tweets': tweets,
    }
    return render(request, 'pages/all_tweets.html', context)


def user_page(request, username):
    # CREATE tweets
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request,
        # including uploaded files
        form = TweetForm(request.POST, request.FILES)

        if form.is_valid():
            # Use the form to save
            tweet = form.save(commit=False)
            tweet.username = request.user.username
            tweet.save()
            # Cool trick to redirect to the previous page
            return redirect(request.META.get('HTTP_REFERER', '/'))

    else:
        # if a GET we'll create a blank form
        form = TweetForm()

    user = User.objects.get(username=username)

    # READ tweets and User information from database
    # We can break down complicated filtering of "querysets" into multiple
    # lines like this
    tweets = Tweet.objects.order_by('-created')
    tweets_by_user = tweets.filter(username=username)

    context = {
        'tweets': tweets_by_user,
        'form': form,
        'user_on_page': user,
        'is_me': user == request.user,
    }
    return render(request, 'pages/user_page.html', context)



def delete_tweet(request, tweet_id):
    tweet = Tweet.objects.get(id=tweet_id)
    tweet.delete()

    # Redirect to wherever they came from
    return redirect(request.META.get('HTTP_REFERER', '/'))



def update_tweet(request, tweet_id):
    text = request.POST['text']

    # Update the tweet
    tweet = Tweet.objects.get(id=tweet_id)
    tweet.text = text
    tweet.save()

    # Redirect to wherever they came from
    return redirect(request.META.get('HTTP_REFERER', '/'))


def edit_user_profile(request, username):
    # Get the user we are looking for
    user = User.objects.get(username=username)

    if request.method == 'POST':

        # Create a form instance and populate it with data from the request
        form = EditUserForm(request.POST, instance=user)

        if form.is_valid():
            form.save()
            return redirect('/users/' + user.username)

    else:
        # A GET, create a pre-filled form with the instance.
        form = EditUserForm(instance=user)

    context = {
        'form': form,
    }
    return render(request, 'pages/edit_user_profile.html', context)

