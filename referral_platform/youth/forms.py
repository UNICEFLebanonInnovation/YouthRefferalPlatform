from __future__ import unicode_literals, absolute_import, division

from django.utils.translation import ugettext as _
from django import forms

from model_utils import Choices
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions, Accordion, PrependedText, InlineCheckboxes
from crispy_forms.layout import Layout, Fieldset, Button, Submit, Div, Field, HTML
from bootstrap3_datetime.widgets import DateTimePicker

from dal import autocomplete

from referral_platform.youth.models import YoungPerson

YES_NO_CHOICE = ((False, _('No')), (True, _('Yes')))


class RegistrationForm(forms.ModelForm):

    birthdate = forms.DateField(
        widget=DateTimePicker(
            options={
                "format": "DD/MM/YYYY",
                "pickTime": False
            }),
        required=True
    )

    leaving_education_reasons = forms.MultipleChoiceField(
        choices=Choices(
            (_('To help my family in house chores')),
            (_('To help my family in breadwinning')),
            (_('I got low grades or did not pass my exams')),
            (_('I have/had physical or mental health problems')),
            (_('School was too far away')),
            (_('School was too expensive')),
            (_('School was unsafe due to community conflict')),
            (_('School was boring/not appealing to me')),
            (_('I felt discriminated against at school')),
            (_('Other')),
        ),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    employment_sectors = forms.MultipleChoiceField(
        choices=Choices(
            (_('Markets and shops')),
            (_('Agriculture & Fishing')),
            (_('Handicrafts and art crafts (carpentry, wood works, etc)')),
            (_('Manufacturing, factory and machinery')),
            (_('construction and associated industries (plumbing, electrician)')),
            (_('Unskilled labor and basic occupations (shoe cleaners, street sellers, domestic help, etc)')),
            (_('Civil Society')),
            (_("I don't want to answer")),

        ),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    looking_for_work = forms.TypedChoiceField(
        coerce=lambda x: x == 'True',
        choices=YES_NO_CHOICE,
        widget=forms.RadioSelect
    )

    through_whom = forms.MultipleChoiceField(
        choices=Choices(
            (_('Through family and friends')),
            (_('Through an employment office')),
            (_('Through a trainer')),
            (_('Through an NGO that you were trained with')),
            (_('Through the Internet')),
            (_('Other')),
        ),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    obstacles_for_work = forms.MultipleChoiceField(
        choices=Choices(
            ('location', _('The workplace was in an unsafe location')),
            ('salary', _('Low Salary Offered')),
            ('disability', _('Mental or Physical Disability')),
            ('education', _('Low Education Level')),
            ('language', _('Foreign Language')),
            ('opportunities', _('Few Job Opportunities')),
            ('skills', _('Lack of Skills for the job')),
            ('laws', _('Rigid Labour Laws')),
        ),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    supporting_family = forms.TypedChoiceField(
        coerce=lambda x: x == 'True',
        choices=YES_NO_CHOICE,
        widget=forms.RadioSelect
    )

    household_composition = forms.MultipleChoiceField(
        choices=Choices(
            (_('Mother (check)')),
            (_('Father (check)')),
            (_('Sister - # 1, 2, 3')),
            (_('Brother - # 1, 2, 3')),
            (_('Other relatives')),
            (_('No response')),
        ),
        widget=forms.CheckboxSelectMultiple
    )

    # safety_reasons = forms.MultipleChoiceField(
    #     choices=Choices(
    #         (_('conflict-related')),
    #         (_('violence at home')),
    #         (_('harassment/violence by the neighborhood')),
    #         (_('harassment/violence in the school')),
    #         (_('Other')),
    #     ),
    #     widget=forms.CheckboxSelectMultiple
    # )

    # trained_before = forms.TypedChoiceField(
    #     coerce=lambda x: x == 'True',
    #     choices=YES_NO_CHOICE,
    #     widget=forms.RadioSelect
    # )
    #
    # sports_group = forms.TypedChoiceField(
    #     coerce=lambda x: x == 'True',
    #     choices=YES_NO_CHOICE,
    #     widget=forms.RadioSelect
    # )

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['id_type'].empty_label = _('ID Type')
        self.fields['sex'].empty_label = _('Gender')
        self.fields['nationality'].empty_label = _('Nationality')
        self.fields['location'].empty_label = _('Location')
        self.fields['partner_organization'].empty_label = _('Partner Organisation')
        self.fields['education_status'].empty_label = _('Are you currently studying?')
        self.fields['education_type'].empty_label = _('Type of education?')
        self.fields['education_level'].empty_label = _('Current education level?')
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Fieldset(
                _('Basic Data'),
                Div(
                    Div(PrependedText('first_name', _('First Name')), css_class='col-md-4'),
                    Div(PrependedText('father_name', _('Father Name')), css_class='col-md-4'),
                    Div(PrependedText('last_name', _('Last Name')), css_class='col-md-4'),
                    css_class='row',
                ),
                Div(
                    Div(PrependedText('mother_firstname', _('Mother First Name')), css_class='col-md-6'),
                    Div(PrependedText('mother_lastname', _('Mother Last Name')), css_class='col-md-6'),
                    css_class='row',
                ),
                Div(
                    Div(PrependedText('id_number', _('ID Number')), css_class='col-md-6', ),
                    Div('id_type', css_class='col-md-6',),
                    css_class='row',
                ),
                Div(
                    Div(PrependedText('disability', _('Disability')), css_class='col-md-4', ),
                    Div('sex', css_class='col-md-4', ),
                    Div(PrependedText('birthdate', _('Birthdate')), css_class='col-md-4', ),
                    css_class='row',
                ),
                Div(
                    Div('nationality', css_class='col-md-4', ),
                    Div(PrependedText('phone', _('Phone Number')), css_class='col-md-4', ),
                    Div(PrependedText('parents_phone_number', _('Parents Phone Number')), css_class='col-md-4', ),
                    css_class='row',
                ),
                Div(
                    Div('location', css_class='col-md-6', ),
                    Div('partner_organization', css_class='col-md-6', ),
                    css_class='row',
                ),
            ),
            Fieldset(
                _('Educational Information'),
                Div(
                    Div(
                        HTML(_('1. Have you ever attended school or other training programs?')),
                        'education_status', css_class='col-md-4',
                    ),
                    Div(
                        HTML(_('1.a What type of education are/were you enrolled in?')),
                        'education_type', css_class='col-md-4',
                    ),
                    Div(
                        HTML(_('1.b What is the level of education you have successfully completed?')),
                        'education_level', css_class='col-md-4',
                    ),
                    css_class='row',
                ),
                HTML(_('2. What were your reason(s) for stopping studying? Please tick all that apply?')),
                Field('leaving_education_reasons'),
            ),
            Fieldset(
                _('Livelihood Information'),
                Div(
                    Div(
                        HTML(_('1. Relationship with Labour Market')),
                        Field('employment_status'),
                        css_class='col-md-6'),
                    Div(
                        HTML(_('2. What is the sector(s) you worked in / or are working in?')),
                        Field('employment_sectors'),
                        css_class='col-md-6'),
                    css_class='row',
                ),
                Div(
                    Div(
                        HTML(_('3. If you are currently not working, are you searching for work now?')),
                        Div('looking_for_work'),
                        css_class='col-md-6'),
                    Div(
                        HTML(_('3.a If yes, through whom? (select multiple)')),
                        Div('through_whom'),
                        css_class='col-md-6'),
                    css_class='row',
                ),
                Div(
                    Div(
                        HTML(_('4. What are the obstacles in searching for/or having work?')),
                        Div('obstacles_for_work'),
                        css_class='col-md-6'),
                    Div(
                        HTML(_('4.a Do you participate in supporting your family financially?')),
                        Div('supporting_family'),
                        css_class='col-md-6'),
                    css_class='row',
                ),
                Div(
                    Div(
                        HTML(_('5. Please check all the choice(s) that best describes your household composition')),
                        Div('household_composition'),
                        css_class='col-md-6'),
                    Div(
                        HTML(_('6. How many members in your household work?')),
                        Div('household_working'),
                        css_class='col-md-6'),
                    css_class='row',
                ),
            ),
            Fieldset(
                _('Follow-up Availability'),
                Div(
                    Div(
                        HTML(_('1. Have you attended any kind of training before?')),
                        Div('trained_before'),
                        css_class='col-md-6'),
                    Div(
                        HTML(_('1.a If not, why?')),
                        Div('not_trained_reason'),
                        css_class='col-md-6'),
                    css_class='row',
                ),
                Div(
                    Div(
                        HTML(_('How did you know about this program?')),
                        Div('referred_by'),
                        css_class='col-md-6'),
                    Div(
                        HTML(_('4. We would like to follow up with you after the training, what is your preferred method of communication?')),
                        Div('communication_preference'),
                        css_class='col-md-6'),
                    css_class='row',
                ),
            ),
            FormActions(
                Submit('save', _('Save changes')),
                Button('cancel', _('Cancel'))
            )
        )

    def save(self, user=None):
        user_profile = super(RegistrationForm, self).save(commit=False)
        if user:
            user_profile.user = user
        user_profile.save()
        return user_profile

    class Meta:
        model = YoungPerson
        exclude = ('user', 'full_name', 'mother_fullname',)
        widgets = {
            'employment_status': forms.RadioSelect(),
            'sports_group': forms.RadioSelect(),
            'location': autocomplete.ModelSelect2(url='locations:location-autocomplete')
        }
