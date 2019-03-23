from __future__ import print_function
import datetime
from datetime import timedelta
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

from secret_settings import *

from .models import Refill
from .models import RefillEvent


SCOPES = ["https://www.googleapis.com/auth/calendar.events"] #, "https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email"]


class RefillForm(forms.ModelForm):
    class Meta:
        model = Refill
        fields = ['prescription', 'nickname', 'pharmacy', 'refill_date', "refill_time", "all_day", "often", "repeats"]
        



def homepage(request):
    context = {
    }
    return render(request, 'pages/index.html', context)

# apparently we need this
def login(request):
    context={
    }
    return render(request, 'pages/login.html', context)


# currently the only way to logout is to go to '/logout' and it will do it for you
def logout(request):
    auth_logout(request)
    return redirect('/')
    

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

            #make date strings
            date = str(refill.refill_date)
            starttime = str(refill.refill_time)
            hour =(datetime.datetime.combine(datetime.date(1,1,1),refill.refill_time) + timedelta(hours=1)).time()
            endtime = str(hour)
            startdatetime= date + 'T' +starttime +'-07:00' 
            print(date)
            print(startdatetime)
            enddatetime= date + 'T' +endtime +'-07:00'
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
            if refill.nickname is None:
                medname=refill.prescription
            else: 
                medname=refill.nickname
            location= ""
            if refill.pharmacy is None:
                pass
            else:
                location = "at " + refill.pharmacy
            event = { 
                #the event dictionary will look like this, just with the user's info
          'summary': 'Refill: '+ medname,
          'location': refill.pharmacy,
          'description': 'Time to refill '+ medname+' '+ location,
          'start': {
            "date": date,
            'dateTime': startdatetime,
            'timeZone':'America/Los_Angeles'
          },
          'end': {
            "date": date,
            'dateTime': enddatetime,
            'timeZone': 'America/Los_Angeles'
          }, 
            "recurrence": [recurrence
            ],
                }
                # creates and pushes the refill event
            event = service.events().insert(
                            calendarId='primary', body=event).execute()
            print ('Event created: %s' % (event.get('htmlLink')))
            return redirect('/all-refills')

    else:
        # if a GET we'll create a blank form
        form = RefillForm()
    context = {
        'form': form,
    }
    return render(request, 'pages/new_med.html', context)


def view_all_refills(request):
    refills = Refill.objects.order_by('-nickname')
    refills_by_user = refills.filter(user_id=request.user.id)
    context = {
        'refills': refills_by_user,
        'username':request.user.username 
    }
    return render(request, 'pages/all_refills.html', context)
# have to figure out what information we want to display on this page


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
