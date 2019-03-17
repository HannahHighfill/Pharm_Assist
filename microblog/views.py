from __future__ import print_function
#import datetime
#from datetime import timedelta
import pickle
import os.path
import requests
from googleapiclient.discovery import build
from django.shortcuts import render, redirect
from django import forms
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import logout as auth_logout
from google.oauth2 import credentials
from google.oauth2.credentials import Credentials

from .models import Refill
from .models import RefillEvent




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
        fields = ['prescription', 'nickname', 'pharmacy', 'number']
        
class RefillEvent(forms.ModelForm):
    class Meta:
        model = RefillEvent
        fields = ['prescription', 'nickname', 'pharmacy', 'number']
    # the fields will change after we figure out how to auto-populate the event dictionary


# This homepage can end up hosting the calendar, Jamie just put them on separate pages so the info would be easy to find
# currently the homepage logs a user in or says hello to them
def homepage(request):
    #this re-writes the pickle file with the user's credentials
    if request.user.is_authenticated:
        social = request.user.social_auth.get(provider='google-oauth2')
        a_token= social.extra_data['access_token']
        print("a token :", a_token) #
        r_token= social.extra_data['refresh_token']
        print("r token :", r_token) #
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
                print ("creds token:", creds.token) #
                creds.token =  a_token #these are not necessarily the same
                print ("changed creds token:", creds.token) #
                creds._refresh_token = r_token
                print ("creds new refresh token is:", creds.refresh_token) #
                
                if not creds or not creds.valid:
                    if creds and creds.expired and creds.refresh_token:
                        #creds.refresh(Request()) #it broke right here
                        print("creds not refreshed") # haven't seen this run
                with open('token.pickle', 'wb') as token:
                    pickle.dump(creds, token)
                    print("pickle rewritten") #
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
        form = RefillEvent(request.POST)
        if form.is_valid():
            refillevent = form.save(commit=False)
            refillevent.user_id = request.user.id
            refillevent.save()
            
        # Write the form's info into an event on their google calendar
            # load credential from token.pickle and build calendar api
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
                rt = creds._refresh_token #
                print("rt", rt) #
                ex = creds.expired #
                print("ex", ex) #
                print("creds", creds) #
                service = build('calendar', 'v3', credentials=creds)

        # Hannah- instead of this hard-coded event, you need to write code that takes the data from the RefillEvent model (the table in SQLite), sorts it by the user's ID, checks if it is unwritten, populates an event dictionary, writes the event, and marks the event as written. This needs to happen for each unwritten event of the logged in user
                event = { 
                #the event dictionary will look like this, just with the user's info
          'summary': 'Google I/O 2015',
          'location': '800 Howard St., San Francisco, CA 94103',
          'description': 'A chance to hear more about Google\'s developer products.',
          'start': {
            'dateTime': '2019-03-17T09:00:00-07:00',
            'timeZone': 'America/Los_Angeles',
          },
          'end': {
            'dateTime': '2019-03-17T17:00:00-07:00',
            'timeZone': 'America/Los_Angeles',
          }, #there are more fields that can be added
                }
                # creates and pushes the refill event
                event = service.events().insert(
                            calendarId='primary', body=event).execute()
                print ('Event created: %s' % (event.get('htmlLink')))
            return redirect('/') # Currently redirects to homepage

    else:
        # if a GET we'll create a blank form
        form = RefillEvent()
    context = {
        'form': form,
    }
    return render(request, 'pages/new_med.html', context)

def view_all_refills(request):
    refills = Refill.objects.order_by('-created')
    context = {
        'refills': refills,
    }
    return render(request, 'pages/all_refills.html', context)


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

