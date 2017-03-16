# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import User


class PlatformUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class PlatformUserCreationForm(UserCreationForm):

    error_message = UserCreationForm.error_messages.update({
        'duplicate_email': 'This email has already been taken.'
    })

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2',)

    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(self.error_messages['duplicate_email'])


@admin.register(User)
class PlatformUserAdmin(admin.ModelAdmin):
    form = PlatformUserChangeForm
    add_form = PlatformUserCreationForm
    fieldsets = (
            ('User Profile', {'fields': ('first_name',)}),
    ) + AuthUserAdmin.fieldsets
    list_display = ('first_name', 'is_superuser')
    search_fields = ['first_name', 'last_name']
