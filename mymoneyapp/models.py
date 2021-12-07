from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    login_attempts = models.IntegerField(default=0, blank=False)
    banned_until = models.DateTimeField(default=None, blank=True, null=True)
    last_attempt = models.DateTimeField(default=None, blank=True, null=True)

class Category(models.Model):
    id = models.IntegerField(primary_key=True, blank=False, null=False, unique=True)
    category = models.CharField(max_length = 25)

class AccountType(models.Model):
    id = models.IntegerField(primary_key=True, blank=False, null=False, unique=True)
    acc_type = models.CharField(max_length = 25)

class Account(models.Model):
    id = models.AutoField(primary_key=True, blank=False, null=False, unique=True)
    username = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "account_owner")
    acc_type = models.ForeignKey(AccountType, on_delete = models.CASCADE, related_name = "account_type")
    name =  models.CharField(max_length = 25)
    initial_balance = models.DecimalField(max_digits = 10, decimal_places=2)
    current_balance = models.DecimalField(max_digits = 10, decimal_places=2)

class Record(models.Model):
    id = models.AutoField(primary_key=True, blank=False, null=False, unique=True)
    username = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "record_owner")
    account = models.ForeignKey(Account, on_delete = models.CASCADE, related_name = "account_record")
    category = models.ForeignKey(Category, on_delete = models.CASCADE, related_name = "record_category")
    is_income = models.BooleanField(default=False)
    quantity = models.DecimalField(max_digits = 10, decimal_places=2)
    date = models.DateField()
    update_datetime = models.DateTimeField()
    description = models.CharField(max_length = 75)

    
