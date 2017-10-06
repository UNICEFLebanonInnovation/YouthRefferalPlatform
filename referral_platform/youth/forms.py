from __future__ import unicode_literals, absolute_import, division

from django.utils.translation import ugettext as _
from django import forms
from referral_platform.youth.models import YoungPerson


class RegistrationForm(forms.ModelForm):

    class Meta:
        model = YoungPerson
        exclude = ('user', 'full_name', 'mother_fullname',)
        widgets = {
            'employment_status': forms.RadioSelect(),
            'sports_group': forms.RadioSelect(),
            # 'location': autocomplete.ModelSelect2(url='locations:location-autocomplete')
        }

    class Media:
        js = ()
