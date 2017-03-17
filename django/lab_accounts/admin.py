from django import forms
from django.contrib import admin

from lab_accounts.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'identity_card',
            'username',
            'password',
            'email'
        ]


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    form = UserForm
