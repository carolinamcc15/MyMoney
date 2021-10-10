from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

# Create your views here.
def index(request):
    return render(request, 'landing.html')

def sign_up(request):
    return render(request, 'sign-up.html')

def login(request):
    return render(request, 'login.html')

def general(request):
    return render(request, 'general.html')

def add_account(request):
    return render(request, 'add-account.html')

def add_record(request):
    return render(request, 'add-record.html')

