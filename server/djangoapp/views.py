from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .restapis import post_request, get_dealers_from_cf, get_dealer_by_id_from_cf, get_dealer_by_state_from_cf, get_dealer_reviews_from_cf, analyze_review_sentiments
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.

# Create an `about` view to render a static about page
def about(request):
    context = {}
    return render(request, 'djangoapp/about.html')

# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    return render(request, 'djangoapp/contact.html')

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return render(request, 'djangoapp/index.html', context)
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'onlinecourse/login.html', context)
    else:
        return render(request, 'djangoapp/login.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    context = {}
    logout(request)
    return render(request, 'djangoapp/logout.html', context)

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.debug("{} is new user".format(username))
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return render(request, 'djangoapp/index.html', context)
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        dealerId = request.GET.get('dealerId', '')
        state = request.GET.get('state', '')
        url = "https://prolactin-3000.theianext-0-labs-prod-misc-tools-us-east-0.proxy.cognitiveclass.ai/dealerships/get"
        # Get dealers from the URL
        dealerships = []
        if dealerId != '' :
            dealerships = get_dealer_by_id_from_cf(url, dealerId)
        elif state != '': 
            dealerships = get_dealer_by_state_from_cf(url, state)
        else:
            dealerships = get_dealers_from_cf(url)
        
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        url = "https://prolactin-3000.theianext-0-labs-prod-misc-tools-us-east-0.proxy.cognitiveclass.ai/dealerships/get"
        # Get dealers from the URL
        dealerships = get_dealer_by_id_from_cf(url, dealer_id)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)

def get_dealer_reviews(request, dealer_id):
    if request.method == "GET":
        url = "https://prolactin-5000.theianext-0-labs-prod-misc-tools-us-east-0.proxy.cognitiveclass.ai/api/get_reviews"
        # Get dealers from the URL
        dealerships = get_dealer_reviews_from_cf(url, dealer_id)
        print(dealerships)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.review for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)

def test_reviews(request):
    if request.method == "GET":
        url = "https://prolactin-5000.theianext-0-labs-prod-misc-tools-us-east-0.proxy.cognitiveclass.ai/api/get_reviews"
        sentiment = analyze_review_sentiments('This is a great car dealer')      
        return HttpResponse(sentiment)

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    print('dealerid')
    print(dealer_id)
    context = {}
    url = "https://prolactin-5000.theianext-0-labs-prod-misc-tools-us-east-0.proxy.cognitiveclass.ai/api/post_review"
    if request.method == "POST":
        params = dict()
        params["id"] = 1115
        params["name"] = request.POST['name']
        params["dealership"] = dealer_id
        params["review"] = request.POST['review']
        params["purchase"] = True
        params["another"] = "field"
        params["purchase_date"] = "02/16/2021"
        params["car_make"] = "Audi"
        params["car_model"] = "Car"
        params["car_year"] = 2021

        json_payload = dict()
        json_payload["review"] = params

        response = post_request(url, params, dealerId=dealer_id)

        print(response);

        context['message'] = "Review added successuly!"
        context['dealerid'] = dealer_id
        return render(request, 'djangoapp/add_review.html', context)
    else:
        context['dealerid'] = dealer_id
        return render(request, 'djangoapp/add_review.html', context)
