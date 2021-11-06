from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db import IntegrityError
from django.utils.timezone import make_aware

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
        "user": user
    })

@login_required
def add_account(request):
    if request.method == "POST":
        changed_value = False
        blank = False

        try:
            acc_type =  request.POST['account-type']
            name = request.POST['account-name']
            balance = request.POST['balance']
            acc_type = AccountType.objects.get(acc_type = acc_type)
            float(balance)
        except:
            changed_value = True
            return render(request, 'message.html')

        if (len(name) > 0 and len(name) <= 20 and name != "") and (float(balance) >= 0 and balance != None) and not changed_value:
            new_account = Account(
            username =request.user, 
            acc_type = acc_type, 
            name = name, 
            initial_balance = balance, 
            current_balance = balance)

            new_account .save()

            return HttpResponseRedirect(reverse("general"))

        else:
            if name == "" or balance == "" or acc_type == "":
                blank = True
            
            return render(request, 'add-account.html', {
                "types": AccountType.objects.all(),
                "error": True,
                "name": name,
                "balance": balance, 
                "blank": blank
            })

    return render(request, 'add-account.html', {
        "types": AccountType.objects.all(),
        "error": False,
        "name": "",
        "balance": "",
        "blank": False
    })
    
@login_required
def account(request, id):
    current_account = Account.objects.get(id = id)
    records = Record.objects.filter(account = current_account).order_by('-update_datetime')
    changedValue = False
    blank = False
    
    if request.method == "POST" and "edit-account" in request.POST:
        try:
            acc_type =  str.strip(request.POST['account-type'])
            name = str.strip(request.POST['account-name'])
            balance = str.strip(request.POST['balance'])
            acc_type = AccountType.objects.get(acc_type = acc_type)
            float(balance)
        except:
            changedValue = True
            return render(request, 'message.html')

        if (len(name) > 0 and len(name) <= 20 and name != None) and (float(balance) >= 0 and balance != None) and not changedValue:
            Account.objects.filter(id = id).update(
            username = request.user, 
            acc_type = acc_type, 
            name = name,
            initial_balance = balance, 
            current_balance = balance,
            )

            return HttpResponseRedirect(reverse("general"))
        
        else:
            if name == "" or balance == "" or acc_type == "":
                blank = True

            return render(request, 'account.html', {
            "account": current_account,
            "types": AccountType.objects.all(),
            "records": records,
            "norecords": "No se encontraron registros",
            "error": True,
            "blank": blank
            })

    elif request.method == "POST" and "delete-account" in request.POST:
        Account.objects.filter(id = id).delete()

        return HttpResponseRedirect(reverse("general"))

    return render(request, 'account.html', {
        "account": current_account,
        "types": AccountType.objects.all(),
        "records": records,
        "norecords": "No se encontraron registros",
        "error": False,
        "blank": False
    })

@login_required
def add_record(request):
    if request.method == "POST":
        not_enough = False
        error = False

        try:
            category =  request.POST['category']
            account = request.POST['account']
            is_income = request.POST.get("is-income", None)
            quantity = request.POST['quantity']
            description = request.POST['description']
            user = request.user

            category = Category.objects.get(category = category)
            selected_account = Account.objects.get(name = account, username = user)
            balance = selected_account.current_balance

            float(quantity)

        except:
            return render(request, 'message.html')

        if float(quantity) < 0 or (float(quantity) > float(balance) and is_income == 'False'):
            if float(quantity) > float(balance) and is_income == 'False':
                not_enough = True

            if float(quantity) < 0:
                error = True

            return render(request, 'add-record.html', {
                "categories": Category.objects.all(),
                "accounts": Account.objects.filter(username = request.user),
                "not_enough": not_enough,
                "error": error
            })

        else:
            new_record = Record(
                username =request.user, 
                account = selected_account,
                category = category,
                is_income = is_income,
                quantity = quantity, 
                date = datetime.datetime.now().strftime("%Y-%m-%d"),
                update_datetime = datetime.datetime.now(),
                description = description
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
        "accounts": Account.objects.filter(username = request.user),
        "not_enough": False, 
        "error": False
    })


@login_required
def edit_record(request, id):
    current_record = Record.objects.get(id = id)

    if request.method == "POST" and "edit-record" in request.POST:
        try:
            category =  request.POST['category']
            account = request.POST['account']
            is_income = request.POST.get("is-income", None)
            quantity = request.POST['quantity']
            description = request.POST['description']
            user = request.user

            category = Category.objects.get(category = category)
            selected_account = Account.objects.get(name = account, username = user)
            balance = selected_account.current_balance

            float(quantity)

        except:
            return render(request, 'message.html')

        if float(quantity) < 0 or (float(quantity) > float(balance) and is_income == 'False'):
            if float(quantity) > float(balance) and is_income == 'False':
                not_enough = True

            if float(quantity) < 0:
                error = True

            return render(request, 'add-record.html', {
                "categories": Category.objects.all(),
                "accounts": Account.objects.filter(username = request.user),
                "not_enough": not_enough,
                "error": error
            })
        else:
            Record.objects.filter(id = id).update(
                username = request.user, 
                account = selected_account,
                category = category,
                is_income = is_income,
                quantity = request.POST['quantity'],
                description = description
                )

            if is_income == 'False':
                selected_account.current_balance = balance - float(quantity)
            else:
                selected_account.current_balance = balance + float(quantity)

            selected_account.save()

            return HttpResponseRedirect(reverse("general"))

    elif request.method == "POST" and "delete-record" in request.POST:
        account = Account.objects.get(id = current_record.account.id)

        if current_record.is_income:
            account.current_balance = float(account.current_balance) - float(current_record.quantity)
        else:
            account.current_balance = float(account.current_balance) + float(current_record.quantity)

        account.save()

        Record.objects.filter(id = id).delete()

        return HttpResponseRedirect(reverse("general"))

    return render(request, 'edit-record.html', {
        "record": current_record,
        "categories": Category.objects.all(),
        "accounts": Account.objects.filter(username = request.user),
        "not_enough": False, 
        "error": False
    })

def sign_up(request):
    if request.method == 'POST':
        try:
            username = str.strip(request.POST['username'])
            email = str.strip(request.POST['email'])
            password = str.strip(request.POST['password'])
            confirm = str.strip(request.POST['confirm-password'])
        except:
            return render(request, 'message.html')

        email_msg = False
        username_msg = False
        password_msg = False
        insecure_password = False
        blank_field = False

        if username == "" or email == "" or password == "" or confirm == "":
            blank_field = True

        # Regex validation
        email_pattern = "^[a-zA-Z0-9.!#$%&’*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$"
        username_pattern = "^[a-zA-Z0-9_-]*$"
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
                "insecure_password": insecure_password,
                "blank": blank_field
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
                "insecure_password": insecure_password,
                "blank": blank_field
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
                "insecure_password": False,
                "blank": False
            })

def log_in(request):
    banned = False
    minutes = ""
    if request.method == "POST":
        try:
            username = str.strip(request.POST['username'])
            password = str.strip(request.POST['password'])
        except:
            blank_fields = False
            return render(request, 'message.html')

        if username != "" and password != "":
            user = authenticate(request, username = username, password = password)
        else:
            blank_fields = True
            return render(request, 'login.html', {
                            "failed": True,
                            "username": username,
                            "blank": blank_fields,
                            "submit": "disabled" if banned else "",
                            "banned": banned,
                            "remaining": minutes if banned else ""
            })

        if user is not None:
            if user.banned_until is None:
                login(request, user)
                User.objects.filter(username = username).update(
                    login_attempts = 0
                )
                return HttpResponseRedirect(reverse("general"))

            #Si ya pasaron los 15 minutos
            elif user.banned_until is not None and user.banned_until < make_aware(datetime.datetime.now()):
                User.objects.filter(username = username).update(
                        login_attempts = 0,
                        banned_until = None
                )

                login(request, user)

                return HttpResponseRedirect(reverse("general"))

            else:
                banned = True

                if user.banned_until is not None:
                    remaining = user.banned_until - make_aware(datetime.datetime.now())
                    minutes = (remaining.seconds % 3600) // 60

                return render(request, 'login.html', {
                    "failed": False,
                    "username": "",
                    "blank": False,
                    "submit": "disabled" if banned else "",
                    "banned": banned,
                    "remaining": minutes if banned else ""
                })

        else:
            #Comprobar si el usuario se encuentra en la bd
            if User.objects.filter(username = username).exists():
                curr_user = User.objects.get(username = username)
                last_attempt = curr_user.last_attempt

                if last_attempt is not None:
                    diff = make_aware(datetime.datetime.now()) - last_attempt

                    # Si el usuario no intenta ingresar en más de 15 minutos, se reinician los intentos
                    if diff >= datetime.timedelta(minutes=15) and curr_user.banned_until is None:
                        User.objects.filter(username = username).update(
                                login_attempts = 0,
                                banned_until = None
                        )
                        curr_user.login_attempts = 0;
                        
                if curr_user.login_attempts < 5 and curr_user.banned_until is None:
                    User.objects.filter(username = username).update(
                        login_attempts = curr_user.login_attempts + 1,
                        banned_until = None
                    )
                    banned = False
                elif curr_user.login_attempts >= 5 and curr_user.banned_until is None:
                    User.objects.filter(username = username).update(
                        banned_until = datetime.datetime.now() + datetime.timedelta(minutes = 15)
                    )
                    banned = True
                    remaining = (datetime.datetime.now() + datetime.timedelta(minutes = 15)) - datetime.datetime.now()

                if curr_user.banned_until is not None and curr_user.banned_until <= make_aware(datetime.datetime.now()):
                    User.objects.filter(username = username).update(
                        login_attempts = 1,
                        banned_until = None
                    )
                    banned = False
                elif curr_user.banned_until is not None and curr_user.banned_until > make_aware(datetime.datetime.now()):
                    banned = True
                    remaining = curr_user.banned_until - make_aware(datetime.datetime.now())
                    minutes = (remaining.seconds % 3600) // 60

                User.objects.filter(username = username).update(
                        last_attempt = datetime.datetime.now()
                    )

                return render(request, 'login.html', {
                    "failed": True,
                    "username": "",
                    "blank": False,
                    "submit": "disabled" if banned else "",
                    "banned": banned,
                    "remaining": minutes if banned else ""
                })

            return render(request, 'login.html', {
                "failed": True,
                "username": "",
                "blank": False,
                "submit": "disabled" if banned else "",
                "banned": banned,
                "remaining": minutes if banned else ""
            })

    else:
        return render(request, 'login.html', {
            "failed": False,
            "username": "",
            "blank": False,
            "submit": "disabled" if banned else "",
            "banned": banned,
            "remaining": minutes if banned else ""
        })

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"), {
})

def error_404(request, exception):
    return render(request, 'not-found.html')
