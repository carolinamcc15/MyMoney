from django.contrib import admin
from .models import User, Category, AccountType, Account, Record

admin.site.register(User)
admin.site.register(Category)
admin.site.register(AccountType)
admin.site.register(Account)
admin.site.register(Record)