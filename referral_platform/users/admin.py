# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import ugettext_lazy as _

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
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', )}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_(''), {'fields': ('locations',)}),
    )
    list_display = ('first_name', 'is_superuser')
    search_fields = ['first_name', 'last_name']
    filter_horizontal = ('groups', 'user_permissions', 'locations', )
