from __future__ import unicode_literals, absolute_import, division

from django.utils.translation import ugettext as _
from django import forms

from model_utils import Choices
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions, Accordion, PrependedText, InlineRadios, InlineField, Alert
from crispy_forms.layout import Layout, Fieldset, Button, Submit, Div, Field, HTML
from bootstrap3_datetime.widgets import DateTimePicker

from .models import YouthLedInitiative

YES_NO_CHOICE = ((False, _('No')), (True, _('Yes')))


class YouthLedInitiativePlanningForm(forms.ModelForm):

    class Meta:
        model = YouthLedInitiative
        fields = '__all__'

    start_date = forms.DateField(
        widget=DateTimePicker(
            options={
                "format": "mm/dd/yyyy",
                "pickTime": False
            }),
        required=True
    )

    needs_resources = forms.TypedChoiceField(
        coerce=lambda x: x == 'True',
        choices=YES_NO_CHOICE,
        widget=forms.RadioSelect
    )

    def __init__(self, *args, **kwargs):
        super(YouthLedInitiativePlanningForm, self).__init__(*args, **kwargs)

        self.fields['partner_organization'].empty_label = _('Partner Organisation')
        self.fields['location'].empty_label = _('Select Location for the initiative')
        self.fields['duration'].empty_label = _('Duration of the initiative')

        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Div(
                Div('partner_organization', css_class='col-md-6', ),
                Div(PrependedText('title', _('Initiative Title')), css_class='col-md-6', ),
                css_class='row',
            ),
            HTML(_('How many group members planned the initiative?')),
            'members',
            'location',
            Div(
                Div(PrependedText('start_date', _('Planned start date')), css_class='col-md-6', ),
                Div('duration', css_class='col-md-6', ),
                css_class='row',
            ),
            Alert(_('The below question is to be answered by the team representative of the initiative'), dismiss=False),
            Div(
                Div(
                    HTML(_('Type of Initiative: (Select All That Apply)')),
                    Div('initiative_type'),
                    css_class='col-md-6'),
                Div(
                    HTML(_('Can you please select the skills that your team used to plan the initiative?')),
                    Div('skill_areas'),
                    css_class='col-md-6'),
                css_class='row',
            ),
            HTML(_('What problem are you solving? How did you choose to do this initiative?')),
            Field('why_this_initiative', placeholder=_('not more than 5 sentences')),

            HTML(_('What organizations, groups, or other people will you collaborate with on this project?')),
            'other_groups',

            HTML(_('How many direct beneficiaries will benefit from your planned initiative?')),
            'number_of_beneficiaries',

            HTML(_('Please select the age Groups of the beneficiaries')),
            'age_of_beneficiaries',

            HTML(_('Sex of beneficiaries')),
            'sex_of_beneficiaries',

            HTML(_('How many indirect beneficiaries will benefit from your planned initiative?')),
            'indirect_beneficiaries',

            HTML(_('Are you planning to mobilize resources for this project?')),
            'needs_resources',

            HTML(_('If so, from whom?')),
            'resources_from',

            HTML(_('What kind of support are you planning to receive? (you can select more than one option)')),
            'resources_type',

            HTML(_('Can you please tell us what your initiative is about, its objective and why is it important?')),
            Field('description', placeholder=_('not more than 5 sentences')),

            HTML(_('Can you please tell us your planned results?')),
            Field('planned_results', placeholder=_('not more than 5 sentences')),

            HTML(_('Can you please tell us your anticipated challenges?')),
            Field('anticpated_challenges', placeholder=_('not more than 5 sentences')),

            HTML(_('How are you planning to mitigate those challenges?')),
            Field('mitigation_of_challenges', placeholder=_('not more than 5 sentences')),

            HTML(_('How are you planning to measure progress achieved against your results?')),
            Field('how_to_measure_progress', placeholder=_('not more than 5 sentences')),

            HTML(_('How will you ensure the project is sustainable?')),
            Field('how_to_ensure_sustainability', placeholder=_('not more than 5 sentences')),

            FormActions(
                Submit('save', _('Save')),
                Button('cancel', _('Cancel'))
            )
        )


