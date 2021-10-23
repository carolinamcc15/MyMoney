from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db import IntegrityError

import datetime
import re

from .functions import categories
from .functions import account_types
from .functions import get_data

from .models import User, Category, AccountType, Account, Record

# Create your views here.
def index(request):
    user = request.user

    categories.populate_categories()
    account_types.populate_types()

    if user.is_authenticated:
        return HttpResponseRedirect(reverse("general"))

    return render(request, 'landing.html')


@login_required
def general(request):
    user = request.user
    accounts = Account.objects.filter(username = user)
    total = 0

    recent_records = get_data.recent(user)
    top_categories = get_data.top_categories(user)

    for account in accounts:
        total = total + account.current_balance

    return render(request, 'general.html', {
        "accounts": accounts,
        "total": total,
        "recent_records": recent_records,
        "top": top_categories,
        "norecords": "No se encontraron registros",
    })


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
def account(request, id):
    current_account = Account.objects.get(id = id)
    records = Record.objects.filter(account = current_account).order_by('-update_datetime')
    
    if request.method == "POST" and "edit-account" in request.POST:
        acc_type =  str.strip(request.POST['account-type'])

        Account.objects.filter(id = id).update(
            username =request.user, 
            acc_type = AccountType.objects.get(acc_type = acc_type), 
            name = request.POST['account-name'], 
            initial_balance = request.POST['balance'], 
            current_balance = request.POST['balance']
            )

        return HttpResponseRedirect(reverse("general"))

    elif request.method == "POST" and "delete-account" in request.POST:
        Account.objects.filter(id = id).delete()

        return HttpResponseRedirect(reverse("general"))

    return render(request, 'account.html', {
        "account": current_account,
        "types": AccountType.objects.all(),
        "records": records,
        "norecords": "No se encontraron registros"
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

        if float(quantity) > float(balance) and is_income:
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
            update_datetime = datetime.datetime.now(),
            description = request.POST['description']
        )
        new_record .save()

        if is_income == 'False':
            selected_account.current_balance = float(balance) - float(quantity)
        else:
            selected_account.current_balance = float(balance) + float(quantity)

        selected_account.save()

        return HttpResponseRedirect(reverse("general"))

    return render(request, 'add-record.html', {
        "categories": Category.objects.all(),
        "accounts": Account.objects.filter(username = request.user)
    })


@login_required
def edit_record(request, id):
    current_record = Record.objects.get(id = id)

    if request.method == "POST" and "edit-record" in request.POST:
        category =  str.strip(request.POST['category'])
        account =  str.strip(request.POST['account'])
        is_income = request.POST.get("is-income", None)
        quantity = request.POST['quantity']

        selected_account = Account.objects.get(name = account)
        balance = float(selected_account.current_balance)

        if float(quantity) > float(balance) and is_income == 'False':
            return render(request, 'message.html', {
                "message": "El dinero en la cuenta no alcanza"
            })

        Record.objects.filter(id = id).update(
            username =request.user, 
            account = selected_account,
            category = Category.objects.get(category = category),
            is_income = is_income,
            quantity = request.POST['quantity'],
            description = request.POST['description']
            )

        if is_income == 'False':
            selected_account.current_balance = balance - float(quantity)
        else:
            selected_account.current_balance = balance + float(quantity)

        selected_account.save()

        return HttpResponseRedirect(reverse("general"))

    elif request.method == "POST" and "delete-record" in request.POST:
        # if current_record.is_income:
        #     current_record.account.current_balance = current_record.account.current_balance - float(quantity)
        # else:
        #     current_record.account.current_balance = current_record.account.current_balance + float(quantity)

        Record.objects.filter(id = id).delete()

        return HttpResponseRedirect(reverse("general"))

    return render(request, 'edit-record.html', {
        "record": current_record,
        "categories": Category.objects.all(),
        "accounts": Account.objects.filter(username = request.user)
    })


def sign_up(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm = request.POST['confirm-password']

        email_msg = False
        username_msg = False
        password_msg = False
        insecure_password = False

        # Regex validation
        email_pattern = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
        username_pattern = "^(?=[a-zA-Z0-9._]{8,20}$)(?!.*[_.]{2})[^_.].*[^_.]$"
        password_pattern = "((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W]).{8,20})"
        
        if not re.search(email_pattern, email):
            email_msg = True

        if not re.search(username_pattern, username):
            username_msg = True

        if not re.search(password_pattern, password):
            insecure_password = True

        if password != confirm:
            password_msg = True
        
        if email_msg or username_msg or insecure_password or password_msg:
            return render(request, 'sign-up.html', {
                "username": username,
                "email": email,
                "username_msg": username_msg,
                "taken": False,
                "email_msg": email_msg,
                "password_msg": password_msg,
                "insecure_password": insecure_password
            })

        try:
            new_user = User.objects.create_user(username, email, password)
            new_user.save()
                
        except IntegrityError:
            return render(request, 'sign-up.html', {
                "username": username,
                "email": email,
                "username_msg": username_msg,
                "taken": True,
                "email_msg": email_msg,
                "password_msg": password_msg,
                "insecure_password": insecure_password
            })

        login(request, new_user)

        return HttpResponseRedirect(reverse("general"))
    else:
        return render(request, 'sign-up.html', {
                "username": "",
                "email": "",
                "username_msg": False,
                "taken": False,
                "email_msg": False,
                "password_msg": False,
                "insecure_password": False
            })


def log_in(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("general"))
        else:
            return render(request, 'login.html', {
                "failed": True,
                "username": username
            })
    else:
        return render(request, 'login.html', {
            "failed": False,
            "username": ""
        })


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"), {
})

def error_404(request, exception):
    return render(request, 'not-found.html')