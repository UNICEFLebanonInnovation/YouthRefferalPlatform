from __future__ import unicode_literals, absolute_import, division

from django.utils.translation import ugettext as _
from django import forms
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.contrib import messages
from django.utils.translation import ugettext as _t
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.widgets import FilteredSelectMultiple
from collections import OrderedDict
from crispy_forms.layout import Fieldset, Submit, Div, HTML, Layout
from referral_platform.registrations.models import Assessment, Registration, AssessmentHash
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions, Accordion, PrependedText, InlineRadios, InlineField, Alert
from .models import YouthLedInitiative, YoungPerson, Location
from referral_platform.initiatives.models import AssessmentSubmission

YES_NO_CHOICE = ((False, _('No')), (True, _('Yes')))


class YouthLedInitiativePlanningForm(forms.ModelForm):
    Participants = forms.ModelMultipleChoiceField(queryset=Registration.objects.all(), widget=FilteredSelectMultiple("Participants", is_stacked=False))
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
