from django.contrib import admin
from .models import User, Category, AccountType, Account, Record

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category')

class AccountTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'acc_type')

class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'acc_type', 'name', 'initial_balance', 'current_balance')

class RecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'account', 'category', 'is_income', 'quantity', 'date', 'description')

admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(AccountType, AccountTypeAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Record, RecordAdmin)