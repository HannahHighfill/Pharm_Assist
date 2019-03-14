from django.shortcuts import render, redirect
from django import forms
from django.contrib.auth.models import User
from django.contrib import auth

from .models import Tweet



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

