from django.contrib import admin
from lab_accounts.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass