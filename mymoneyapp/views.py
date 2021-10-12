from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import datetime
from django.db import IntegrityError

from .models import User, Category, AccountType, Account, Record

# Create your views here.
def index(request):
    user = request.user

    if user.is_authenticated:
        return HttpResponseRedirect(reverse("general"))

    return render(request, 'landing.html')


@login_required
def general(request):
    user = request.user
    accounts = Account.objects.filter(username = user)
    records = Record.objects.filter(username = user)
    total = 0
    recent_records = []
    
    for account in accounts:
        total = total + account.current_balance

    for i in range(len(records) - 1, len(records) - 5, -1):
        recent_records.append(records[i])

    return render(request, 'general.html', {
        "accounts": accounts,
        "total": total,
        "recent_records": recent_records
    })


@login_required
def account(request, id):
    current_account = Account.objects.get(id = id)
    if request.method == "POST":
        acc_type =  str.strip(request.POST['account-type'])

        Account.objects.filter(id = id).update(
            username =request.user, 
            acc_type = AccountType.objects.get(acc_type = acc_type), 
            name = request.POST['account-name'], 
            initial_balance = request.POST['balance'], 
            current_balance = request.POST['balance']
            )

        return HttpResponseRedirect(reverse("general"))

    return render(request, 'account.html', {
        "account": current_account,
        "types": AccountType.objects.all()
    })


@login_required
def edit_record(request):
    return render(request, 'edit-record.html')


@login_required
def add_account(request):
    if request.method == "POST":
        acc_type =  request.POST['account-type']

        new_account = Account(
            username =request.user, 
            #Gets the selected category
            acc_type = AccountType.objects.get(acc_type = acc_type), 
            name = request.POST['account-name'], 
            initial_balance = request.POST['balance'], 
            current_balance = request.POST['balance'])

        new_account .save()
        return HttpResponseRedirect(reverse("general"))

    return render(request, 'add-account.html', {
        "types": AccountType.objects.all()
    })


@login_required
def add_record(request):
    if request.method == "POST":
        category =  request.POST['category']
        account = request.POST['account']
        is_income = request.POST.get("is-income", None)
        quantity = request.POST['quantity']

        selected_account = Account.objects.get(name = account)
        balance = selected_account.current_balance

        if int(quantity) > balance and is_income == 'False':
            return render(request, 'message.html', {
                "message": "El dinero en la cuenta no alcanza"
            })
        
        new_record = Record(
            username =request.user, 
            account = selected_account,
            category = Category.objects.get(category = category),
            is_income = is_income,
            quantity = quantity, 
            date = datetime.datetime.now().strftime("%Y-%m-%d"),
            description = request.POST['description']
        )
        new_record .save()

        if is_income == 'False':
            selected_account.current_balance = balance - int(quantity)
        elif is_income == 'True':
            selected_account.current_balance = balance + int(quantity)

        selected_account.save()

        return HttpResponseRedirect(reverse("general"))

    return render(request, 'add-record.html', {
        "categories": Category.objects.all(),
        "accounts": Account.objects.filter(username = request.user)
    })

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


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"), {
})
