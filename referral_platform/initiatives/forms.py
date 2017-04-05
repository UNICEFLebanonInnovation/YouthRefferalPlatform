from __future__ import unicode_literals, absolute_import, division

from django.utils.translation import ugettext as _
from django import forms

from model_utils import Choices
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions, Accordion, PrependedText, InlineRadios, InlineField, InlineCheckboxes
from crispy_forms.layout import Layout, Fieldset, Button, Submit, Div, Field, HTML

from .models import YouthLedInitiative


class YouthLedInitiativePlanningForm(forms.ModelForm):

    initiative_type = forms.MultipleChoiceField(
        choices=Choices(
            ('basic_services', _('Improving or installing basic services (electricity, water, sanitation, and waste removal)')),
            ('social', _('Enhancing social cohesion')),
            ('environmental', _('Environmental')),
            ('health_services', _('Health Services')),
            ('informational', _('Educational, informational or knowledge sharing')),
            ('advocacy', _('Advocacy or Raising awareness')),
            ('political', _('Political')),
            ('religious', _('Spiritual/Religious')),
            ('culture', _('Artistic/Cultural/Sports')),
            ('safety', _('Enhancing public safety')),
            ('public_spaces', _('Improving Public Spaces (parks, hospitals, buildings, schools, sidewalks)')),
            ('other', _('Other')),
        ),
        widget=forms.CheckboxSelectMultiple
    )

    skill_areas = forms.MultipleChoiceField(
        choices=Choices(
            ('self-management', _('Self-Management')),
            ('teamwork', _('Cooperation & Teamwork')),
            ('creativity', _('Creativity')),
            ('critical_thinking', _('Critical Thinking')),
            ('negotiation', _('Negotiation')),
            ('diversity', _('Respect for diversity')),
            ('decision_making', _('Decision Making')),
            ('participation', _('Participation')),
            ('communication', _('Communication')),
            ('empathy', _('Empathy')),
            ('problem_solving', _('Problem-Solving')),
            ('resilience', _('Resilience')),
        ),
        widget=forms.CheckboxSelectMultiple
    )

    other_groups = forms.MultipleChoiceField(
        choices=Choices(
            ('ngos', _('Other NGOs')),
            ('schools', _('Schools')),
            ('municipality', _('Municipality')),
            ('other', _('Other')),
        ),
        widget=forms.CheckboxSelectMultiple
    )

    needs_resources = forms.TypedChoiceField(
        coerce=lambda x: x == 'True',
        choices=((False, 'No'), (True, 'Yes')),
        widget=forms.RadioSelect
    )

    def __init__(self, *args, **kwargs):
        super(YouthLedInitiativePlanningForm, self).__init__(*args, **kwargs)

        self.fields['partner_organization'].empty_label = '1. Partner Organisation'
        self.fields['location'].empty_label = '4. Select Location for the initiative'
        self.fields['duration'].empty_label = '6. Duration of the initiative'

        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Div(
                Div('partner_organization', css_class='col-md-6', ),
                Div(PrependedText('title', '2. Initiative Title'), css_class='col-md-6', ),
                css_class='row',
            ),
            HTML("<p>3. How many group members planned the initiative?</p>"),
            'members',
            'location',
            Div(
                Div(PrependedText('start_date', '5. Planned start date'), css_class='col-md-6', ),
                Div('duration', css_class='col-md-6', ),
                css_class='row',
            ),
            Div(
                Div(
                    HTML("<p>7. Type of Initiative: (Select All That Apply)</p>"),
                    Div('initiative_type'),
                    css_class='col-md-6'),
                Div(
                    HTML("<p>8. Can you please select the skills that your team used to plan the initiative?</p>"),
                    Div('skill_areas'),
                    css_class='col-md-6'),
                css_class='row',
            ),
            HTML("<p>9. What problem are you solving? How did you choose to do this initiative?</p>"),
            Field('why_this_initiative', placeholder='not more than 5 sentences'),

            HTML("<p>10. What organizations, groups, or other people will you collaborate with on this project?</p>"),
            'other_groups',

            HTML("<p>11. How many direct beneficiaries will benefit from your planned initiative?</p>"),
            'number_of_beneficiaries',

            HTML("<p>12. Please select the age Groups of the beneficiaries</p>"),
            'age_of_beneficiaries',

            HTML("<p>13. Sex of beneficiaries</p>"),
            'sex_of_beneficiaries',

            HTML("<p>14. How many indirect beneficiaries will benefit from your planned initiative?</p>"),
            'indirect_beneficiaries',

            HTML("<p>15. Are you planning to mobilize resources for this project?</p>"),
            'needs_resources',

            HTML("<p>15.a If so, from whom?</p>"),
            'resources_from',

            HTML("<p>16. What kind of support are you planning to receive? (you can select more than one option)</p>"),
            'resources_type',

            HTML("<p>17. Can you please tell us what your initiative is about, its objective and why is it important?</p>"),
            Field('description', placeholder='not more than 5 sentences'),

            HTML("<p>18. Can you please tell us your planned results?</p>"),
            Field('planned_results', placeholder='not more than 5 sentences'),

            HTML("<p>19. Can you please tell us your anticipated challenges?</p>"),
            Field('anticpated_challenges', placeholder='not more than 5 sentences'),

            HTML("<p>20. How are you planning to mitigate those challenges?</p>"),
            Field('mitigation_of_challenges', placeholder='not more than 5 sentences'),

            HTML("<p>21. How are you planning to measure progress achieved against your results?</p>"),
            Field('how_to_measure_progress', placeholder='not more than 5 sentences'),

            HTML("<p>22. How will you ensure the project is sustainable?</p>"),
            Field('how_to_ensure_sustainability', placeholder='not more than 5 sentences'),

            FormActions(
                Submit('save', 'Save changes'),
                Button('cancel', 'Cancel')
            )
        )

    class Meta:
        model = YouthLedInitiative
        fields = '__all__'

