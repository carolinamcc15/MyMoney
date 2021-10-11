from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.db import IntegrityError

from .models import User, Category, AccountType, Account, Record

# Create your views here.
def index(request):
    return render(request, 'landing.html')

def sign_up(request):
    if request.method == 'POST':
        username = request.POST['username']
        name = request.POST['name'].split(sep=" ", maxsplit=1)
        email = request.POST['email']
        password = request.POST['password']
        confirm = request.POST['confirm-password']

        if password != confirm:
            return render(request, 'message.html', {
                "message": "Passwords do not match"
            })
        
        try:
            new_user = User.objects.create_user(username, email, password)
            new_user.first_name = name[0]
            new_user.last_name = name[1]
            new_user.save()

        except IntegrityError:
            return render(request, "message.html", {
                "message": "Username already taken."
            })
        login(request, new_user)
        return HttpResponseRedirect(reverse("general"))
    else:
        return render(request, 'sign-up.html')

def log_in(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

            # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("general"))
        else:
            return render(request, "message.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"), {
})

def general(request):
    return render(request, 'general.html')

def account(request):
    return render(request, 'account.html')

def edit_record(request):
    return render(request, 'edit-record.html')

def add_account(request):
    return render(request, 'add-account.html', {
        "types": AccountType.objects.all()
    })

def add_record(request):
    return render(request, 'add-record.html', {
        "categories": Category.objects.all(),
        "accounts": Account.objects.all()
    })

