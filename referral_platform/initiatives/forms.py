from __future__ import unicode_literals, absolute_import, division

from django.utils.translation import ugettext as _
from django import forms
from django.core.urlresolvers import reverse
from django.contrib import messages
from collections import OrderedDict
from dal import autocomplete
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import Layout, Fieldset, Button, Submit, Div, Field, HTML


from django import forms
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.contrib import messages
from django.utils.translation import ugettext as _t
from django.utils.translation import ugettext_lazy as _

from datetime import datetime
from collections import OrderedDict
from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Fieldset, Submit, Div, HTML, Layout

from referral_platform.locations.models import Location
from referral_platform.partners.models import Center
from referral_platform.registrations.models import Assessment, AssessmentSubmission
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

from referral_platform.youth.models import YoungPerson, Nationality, Center
from referral_platform.registrations.models import Registration
from django.utils.safestring import mark_safe
from model_utils import Choices
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions, Accordion, PrependedText, InlineRadios, InlineField, Alert
from bootstrap3_datetime.widgets import DateTimePicker
from .models import YouthLedInitiative, YoungPerson, Location

YES_NO_CHOICE = ((False, _('No')), (True, _('Yes')))


class YouthLedInitiativePlanningForm(forms.ModelForm):

    class Meta:
        model = YouthLedInitiative
        fields = '__all__'


    # start_date = forms.DateField(
    #     widget=DateTimePicker(
    #         options={
    #             "format": "mm/dd/yyyy",
    #             "pickTime": False
    #         }),
    #     required=True
    # )
    #
    # needs_resources = forms.TypedChoiceField(
    #     coerce=lambda x: x == 'True',
    #     choices=YES_NO_CHOICE,
    #     widget=forms.RadioSelect
    # )

    def __init__(self, *args, **kwargs):
        super(YouthLedInitiativePlanningForm, self).__init__(*args, **kwargs)

        self.request = kwargs.pop('request', None)
        instance = kwargs.get('instance', '')
        if instance:
            initials = {}
            initials['partner_locations'] = instance.partner_organization.locations.all()
            initials['partner_organization'] = instance.partner_organization
            # initials['partner_members']=instance



        else:
            initials = kwargs.get('initial', '')

        partner_locations = initials['partner_locations'] if 'partner_locations' in initials else []
        partner_organization = initials['partner'] if 'partner' in initials else 0
        self.fields['location'].queryset = Location.objects.filter(parent__in=partner_locations)
        # self.fields['members'].queryset = YoungPerson.objects.filter(partner_organization=partner_organization)
        my_fields = OrderedDict()

        if not instance:
            my_fields['Search Youth'] = ['search_youth']

        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Div(
                Div('partner_organization', css_class='col-md-6', ),
                Div(PrependedText('title', _('Initiative Title')), css_class='col-md-6', ),
                css_class='row',
            ),
            HTML(_('Please choose the members of this Initiative')),
            'members',
            HTML(_('Location')),
            'location',

            HTML(_('Initiative Type')),
            'type',
            HTML(_('Duration')),
            'duration',)

        self.helper.layout.append(
            FormActions(
                HTML('<a class="btn btn-info col-md-2" href="/initiatives/list/">' + _t('Cancel') + '</a>'),
                Submit('save_add_another', _('Save and add another'), css_class='col-md-2'),
                Submit('save_and_continue', _('Save and continue'), css_class='col-md-2'),
                css_class='btn-actions'

            )
        )

    def save(self, instance=None, request=None):
        super(YouthLedInitiativePlanningForm, self).save()
        messages.success(request, _('Your data has been sent successfully to the server'))






