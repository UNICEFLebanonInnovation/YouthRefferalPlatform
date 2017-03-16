from __future__ import unicode_literals, absolute_import, division

from django.utils.translation import ugettext as _
from django import forms

from model_utils import Choices
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions, Accordion, PrependedText, InlineCheckboxes
from crispy_forms.layout import Layout, Fieldset, Button, Submit, Div, Field, HTML
from bootstrap3_datetime.widgets import DateTimePicker

from dal import autocomplete

from referral_platform.portfolios.models import YoungPerson


class RegistrationForm(forms.ModelForm):

    birthdate = forms.DateField(
        widget=DateTimePicker(
            options={
                "format": "DD/MM/YYYY",
                "pickTime": False
            }))

    leaving_education_reasons = forms.MultipleChoiceField(
        choices=Choices(
            (_('Family Pressure/ Social Norms')),
            (_('Physical or mental health problems')),
            (_('Distance to school')),
            (_('Safety due to conflict')),
            (_('Low standard of schools/Lack of Space')),
            (_('Discrimination at School')),
            (_('Other')),
        ),
        widget=forms.CheckboxSelectMultiple
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
        widget=forms.CheckboxSelectMultiple
    )
    looking_for_work = forms.TypedChoiceField(
        coerce=lambda x: x == 'True',
        choices=((False, 'No'), (True, 'Yes')),
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
        widget=forms.CheckboxSelectMultiple
    )

    obstacles_for_work = forms.MultipleChoiceField(
        choices=Choices(
            ('location', _('Inadequate Location')),
            ('salary', _('Low Salary')),
            ('disability', _('Disability')),
            ('education', _('Low Education Level')),
            ('language', _('Foreign Language')),
            ('opportunities', _('Low Job Opportunities')),
            ('skills', _('Lack of Skills')),
            ('laws', _('Rigid Labour Laws')),
        ),
        widget=forms.CheckboxSelectMultiple
    )
    supporting_family = forms.TypedChoiceField(
        coerce=lambda x: x == 'True',
        choices=((False, 'No'), (True, 'Yes')),
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

    safety_reasons = forms.MultipleChoiceField(
        choices=Choices(
            (_('conflict-related')),
            (_('violence at home')),
            (_('harassment/violence by the neighborhood')),
            (_('harassment/violence in the school')),
            (_('Other')),
        ),
        widget=forms.CheckboxSelectMultiple
    )

    trained_before = forms.TypedChoiceField(
        coerce=lambda x: x == 'True',
        choices=((False, 'No'), (True, 'Yes')),
        widget=forms.RadioSelect
    )

    sports_group = forms.TypedChoiceField(
        coerce=lambda x: x == 'True',
        choices=((False, 'No'), (True, 'Yes')),
        widget=forms.RadioSelect
    )

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['id_type'].empty_label = 'ID Type'
        self.fields['sex'].empty_label = 'Gender'
        self.fields['parents_phone_number'].empty_label = 'Nationality'
        self.fields['location'].empty_label = 'Location'
        self.fields['partner_organization'].empty_label = 'Partner Organisation'
        self.fields['education_status'].empty_label = 'Are you currently studying?'
        self.fields['education_type'].empty_label = 'Type of education?'
        self.fields['education_level'].empty_label = 'Current education level?'
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Fieldset(
                'Basic Data',
                Div(
                    Div(PrependedText('first_name', 'First Name'), css_class='col-md-4'),
                    Div(PrependedText('father_name', 'Father Name'), css_class='col-md-4'),
                    Div(PrependedText('last_name', 'Last Name'), css_class='col-md-4'),
                    css_class='row',
                ),
                Div(
                    Div(PrependedText('mother_firstname', 'Mother First Name'), css_class='col-md-6'),
                    Div(PrependedText('mother_lastname', 'Mother Last Name'), css_class='col-md-6'),
                    css_class='row',
                ),
                Div(
                    Div(PrependedText('id_number', 'ID Number'), css_class='col-md-6', ),
                    Div('id_type', css_class='col-md-6',),
                    css_class='row',
                ),
                Div(
                    Div(PrependedText('disability', 'Disability'), css_class='col-md-4', ),
                    Div('sex', css_class='col-md-4', ),
                    Div(PrependedText('birthdate', 'Birthdate'), css_class='col-md-4', ),
                    css_class='row',
                ),
                Div(
                    Div('nationality', css_class='col-md-4', ),
                    Div(PrependedText('phone', 'Phone Number'), css_class='col-md-4', ),
                    Div(PrependedText('parents_phone_number', 'Parents Phone Number'), css_class='col-md-4', ),
                    css_class='row',
                ),
                Div(
                    Div('location', css_class='col-md-6', ),
                    Div('partner_organization', css_class='col-md-6', ),
                    css_class='row',
                ),
            ),
            Fieldset(
                'Educational Information',
                HTML("<p>Have you been enrolled in any education programme?</p>"),
                Div(
                    Div('education_status', css_class='col-md-4', ),
                    Div('education_type', css_class='col-md-4', ),
                    Div('education_level', css_class='col-md-4', ),
                    css_class='row',
                ),
                HTML("<p>What were your reason(s) for stopping studying? Please tick all that apply?</p>"),
                Div('leaving_education_reasons'),
            ),
            Fieldset(
                'Livelihood Information',
                Div(
                    Div(
                        HTML("<p>1. Relationship with Labour Market*</p>"),
                        Div('employment_status'),
                        css_class='col-md-6'),
                    Div(
                        HTML("<p>2. What is the sector(s) you worked in / or are working in?</p>"),
                        Div('employment_sectors'),
                        css_class='col-md-6'),
                    css_class='row',
                ),
                Div(
                    Div(
                        HTML("<p>3. If you are currently not working, are you searching for work now?*</p>"),
                        Div('looking_for_work'),
                        css_class='col-md-6'),
                    Div(
                        HTML("<p>3.a If yes, through whom? (select multiple)</p>"),
                        Div('through_whom'),
                        css_class='col-md-6'),
                    css_class='row',
                ),
                Div(
                    Div(
                        HTML("<p>4. What are the obstacles in searching for/or having work?*</p>"),
                        Div('obstacles_for_work'),
                        css_class='col-md-6'),
                    Div(
                        HTML("<p>4.a Do you participate in supporting your family financially?</p>"),
                        Div('supporting_family'),
                        css_class='col-md-6'),
                    css_class='row',
                ),
                Div(
                    Div(
                        HTML("<p>5. Please check all the choice(s) that best describes your household composition</p>"),
                        Div('household_composition'),
                        css_class='col-md-6'),
                    Div(
                        HTML("<p>6. How many members in your household work?</p>"),
                        Div('household_working'),
                        css_class='col-md-6'),
                    css_class='row',
                ),
            ),
            Fieldset(
                'Safety and Security Information',
                Div(
                    Div(
                        HTML("<p>1. Which statement applies to you?</p>"),
                        Div('safety'),
                        css_class='col-md-6'),
                    Div(
                        HTML("<p>2. Can you tell us why?</p>"),
                        Div('safety_reasons'),
                        css_class='col-md-6'),
                    css_class='row',
                ),
            ),
            Fieldset(
                'Follow-up Availability',
                Div(
                    Div(
                        HTML("<p>1. Have you attended any kind of training before?</p>"),
                        Div('trained_before'),
                        css_class='col-md-6'),
                    Div(
                        HTML("<p>1.a If not, why?</p>"),
                        Div('not_trained_reason'),
                        css_class='col-md-6'),
                    css_class='row',
                ),
                Div(
                    Div(
                        HTML("<p>2. Are you a part of Sports Group?</p>"),
                        Div('sports_group'),
                        css_class='col-md-6'),
                    Div(
                        HTML("<p>2.a What is the type of sports you practice?</p>"),
                        Div('sport_type'),
                        css_class='col-md-6'),
                    css_class='row',
                ),
                Div(
                    Div(
                        HTML("<p>3. How did you know about this program?</p>"),
                        Div('referred_by'),
                        css_class='col-md-6'),
                    Div(
                        HTML("<p>4. We would like to follow up with you after the training, what is your preferred method of communication?</p>"),
                        Div('communication_preference'),
                        css_class='col-md-6'),
                    css_class='row',
                ),
            ),
            FormActions(
                Submit('save', 'Save changes'),
                Button('cancel', 'Cancel')
            )
        )


    class Meta:
        model = YoungPerson
        exclude = ('user', 'full_name', 'mother_fullname',)
        widgets = {
            'employment_status': forms.RadioSelect(),
            'sports_group': forms.RadioSelect(),
            #'location': autocomplete.ModelSelect2(url='location-autocomplete')

        }
