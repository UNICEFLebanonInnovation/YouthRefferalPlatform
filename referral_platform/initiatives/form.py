from __future__ import unicode_literals, absolute_import, division

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.widgets import FilteredSelectMultiple
from referral_platform.registrations.models import Registration
from .models import YouthLedInitiative

YES_NO_CHOICE = ((False, _('No')), (True, _('Yes')))


class YouthLedInitiativePlanningForm(forms.ModelForm):
    Participants = forms.ModelMultipleChoiceField(queryset=Registration.objects.none(),
                                                  widget=FilteredSelectMultiple("Participants", is_stacked=False))
    search_youth = forms.CharField(
        label=_("Search for youth by name"),
        widget=forms.TextInput,
        required=False
    )
    location = forms.CharField(
        label=_("Location"),
        widget=forms.TextInput,
        required=False
    )
    duration = forms.CharField(
        label=_("Duration"),
        widget=forms.TextInput,
        required=False
    )
    class Meta:
        model = YouthLedInitiative
        fields = '__all__'

    class Media:
        css = {'all': ('/static/admin/css/widgets.css',), }
        js = ('/admin/jsi18n/',)
