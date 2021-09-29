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
