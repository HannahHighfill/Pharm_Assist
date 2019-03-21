from __future__ import print_function
import datetime
from datetime import timedelta
import dateutil
from dateutil.tz import gettz
import pickle
import os.path
import wsgiref
import webbrowser
import json
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google_auth_oauthlib.flow import _RedirectWSGIApp, _WSGIRequestHandler
from wsgiref.simple_server import make_server
from google.auth.transport.requests import Request # All from google api example

from django.shortcuts import render, redirect
from django import forms
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import logout as auth_logout
from google.oauth2 import credentials
from google.oauth2.credentials import Credentials
import httplib2
from django.contrib.auth import authenticate


from .models import Refill
from .models import RefillEvent


SCOPES = ["https://www.googleapis.com/auth/calendar.events"] #, "https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email"]

class NewUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password', 'email']


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class RefillForm(forms.ModelForm):
    class Meta:
        model = Refill
        fields = ['prescription', 'nickname', 'pharmacy', 'refill_date', "timezone", "refill_time", "all_day", "often", "repeats"]
        
class RefillEvent(forms.ModelForm):
    class Meta:
        model = RefillEvent
        fields = ['prescription', 'nickname']
# Jamie think we don't need this


# This homepage can end up hostign the calendar, Jamie just put them on separate pages so the info would be easy to find
#currently the homepage logs a user in or says hello to them
def homepage(request):
    context = {
    }
    return render(request, 'pages/homepage.html', context)



# I do not know if we need this page, given that logging in is happening through google and not through us
def login(request):
    context={
    }
    return render(request, 'pages/login.html', context)


# currently the only way to logout is to go to '/logout' and it will do it for you
def logout(request):
    auth_logout(request)
    return redirect(request.META.get('HTTP_REFERER', '/'))
    
    
#this does not need to be its own page, Jamie just seperated it out so you guys can find all the essential html and code to make the calendar show
def calendar(request):
            context={
                'username':request.user.username 
            }
            return render(request, 'pages/calendar.html', context)

# This page displays the new med form, sends it to the database, and writes the calendar event for the new med
def new_med(request):
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request
        form = RefillForm(request.POST)

        if form.is_valid():
            refill = form.save(commit=False)
            refill.user_id = request.user.id
            refill.save()
            print("form saved")
            
            # Write the form's info into an event on their google calendar
            # if token.pickle exists, don't need rest of login
            if os.path.exists('token.pickle'):
                with open('token.pickle', 'rb') as token:
                    creds = pickle.load(token)
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                flow.redirect_uri = 'http://{}:{}/'.format('localhost',8080)
                print("flow:", flow)
                print("flow:", flow.redirect_uri)
                auth_url, _ = flow.authorization_url(prompt='consent', access_type="offline")
                success_message = "you can close the tab" 
                wsgi_app = _RedirectWSGIApp(success_message) 
                print("wsgi_app:", wsgi_app)
                local_server = wsgiref.simple_server.make_server('localhost', 8080, wsgi_app, handler_class=_WSGIRequestHandler) 
                print("made it past local_server")
                if True:
                    webbrowser.open(auth_url, new=1, autoraise=True)
                authorization_prompt_message = "You can open it at" 
                print("auth url:", auth_url)
                local_server.handle_request() 
                authorization_response = wsgi_app.last_request_uri.replace('http', 'https')
                print ("response url:", authorization_response) 
                flow.fetch_token(authorization_response=authorization_response) 
                creds= flow.credentials 
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

            service = build('calendar', 'v3', credentials=creds)
<<<<<<< HEAD
            #make date strings
            date = str(refill.refill_date)
            starttime = str(refill.refill_time)
            hour =(datetime.datetime.combine(datetime.date(1,1,1),refill.refill_time) + timedelta(hours=1)).time()
            endtime = str(hour)
            timezone = gettz(refill.timezone)
            print(str(timezone))
            startdatetime= date + 'T' +starttime +'Z' #if timezone not in here it will use utc, but place it in los angeles time
            # map timezones to utc offsets. if i just do it in pdt no one will notice. but i will know.
            print(date)
            print(startdatetime)
            enddatetime= date + 'T' +endtime +'Z'
            # all day event
            if refill.all_day == 1:
                startdatetime=None
                enddatetime=None
            else:
                date = None
            # repeating event
            if refill.repeats ==None:
                recurrence = None
            elif refill.often > 0:
                often= str(refill.often)
                recurrence = 'RRULE:FREQ=' + refill.repeats + ';INTERVAL=' + often
            event = { 
          'summary': 'Google I/O 2015',
          'location': '800 Howard St., San Francisco, CA 94103',
          'description': 'A chance to hear more about Google\'s developer products.',
=======
            if refill.nickname is None:
                medname=refill.prescription
            else: 
                medname=refill.nickname
                
            event = { 
                #the event dictionary will look like this, just with the user's info
          'summary': 'Refill:'+ medname,
          'location': refill.pharmacy,
          'description': 'Time to refill '+ medname+' '+ 'at '+ refill.pharmacy,
>>>>>>> master
          'start': {
            "date": date,
            'dateTime': startdatetime,
            'timeZone': refill.timezone
          },
          'end': {
            "date": date,
            'dateTime': enddatetime,
            'timeZone': refill.timezone
          }, 
            "recurrence": [recurrence
            ],
                }
                # creates and pushes the refill event
            event = service.events().insert(
                            calendarId='primary', body=event).execute()
            print ('Event created: %s' % (event.get('htmlLink')))
            return redirect('/calendar')

    else:
        # if a GET we'll create a blank form
        form = RefillForm()
    context = {
        'form': form,
    }
    return render(request, 'pages/new_med.html', context)

<<<<<<< HEAD
def view_all_refills(request): 
    refills = Refill.objects.order_by('-created')
=======
def view_all_refills(request):
    refills = Refill.objects.order_by('-nickname')
>>>>>>> master
    context = {
        'refills': refills,
    }
    return render(request, 'pages/all_refills.html', context)
# have to figure out what information we want to display on this page

def user_page(request, username):
    # CREATE refills
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request,
        # including uploaded files
        form = RefillForm(request.POST, request.FILES)

        if form.is_valid():
            # Use the form to save
            refill = form.save(commit=False)
            refill.username = request.user.username
            refill.save()
            # Cool trick to redirect to the previous page
            return redirect(request.META.get('HTTP_REFERER', '/'))

    else:
        # if a GET we'll create a blank form
        form = RefillForm()

    user = User.objects.get(username=username)

    # READ refills and User information from database
    # We can break down complicated filtering of "querysets" into multiple
    # lines like this
    refills = Refill.objects.order_by('-created')
    refills_by_user = refills.filter(username=username)

    context = {
        'refills': refills_by_user,
        'form': form,
        'user_on_page': user,
        'is_me': user == request.user,
    }
    return render(request, 'pages/user_page.html', context)
# don't think we need this page


def delete_refill(request, refill_id):
    refill = Refill.objects.get(id=refill_id)
    refill.delete()

    # Redirect to wherever they came from
    return redirect(request.META.get('HTTP_REFERER', '/'))



def update_refill(request, refill_id):
    text = request.POST['text']

    # Update the refill
    refill = Refill.objects.get(id=refill_id)
    refill.text = text
    refill.save()

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
#Jamie doesn't think we need this page
