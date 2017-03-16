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
            ('basic_services', _('Basic Services (electricity, water, sanitation, and waste removal)')),
            ('social', _('Social cohesion')),
            ('culture', _('Artistic/Cultural')),
            ('health_services', _('Health Services')),
            ('informational', _('Educational, informational or knowledge sharing')),
            ('advocacy', _('Advocacy')),
            ('political', _('Political')),
            ('religious', _('Spiritual/Religious')),
            ('other', _('Other')),
        ),
        widget=forms.CheckboxSelectMultiple
    )

    knowledge_areas = forms.MultipleChoiceField(
        choices=Choices(
            ('communication', _('Communication')),
            ('teambuilding', _('Team building')),
            ('advocacy', _('Advocacy and mobilization')),
            ('social_cohesion', _('Social cohesion')),
            ('volunteerism', _('Social responsibility and volunteerism')),
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

        self.fields['partner_organization'].empty_label = 'Partner Organisation'
        self.fields['location'].empty_label = 'Select Location for the initiative'
        self.fields['duration'].empty_label = 'Duration of the initiative'

        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Div(
                Div(PrependedText('title', 'Initiative Title'), css_class='col-md-6', ),
                Div('partner_organization', css_class='col-md-6',),
                css_class='row',
            ),
            HTML("<p>How many group members planned the initiative?</p>"),
            'members',
            'location',
            Div(
                Div(PrependedText('start_date', 'Planned start date'), css_class='col-md-6', ),
                Div('duration', css_class='col-md-6', ),
                css_class='row',
            ),
            Div(
                Div(
                    HTML("<p>10. Type of Initiative: (Select All That Apply)</p>"),
                    Div('initiative_type'),
                    css_class='col-md-6'),
                Div(
                    HTML("<p>11. Can you please select the areas of knowledge that this team have used for the planning of the initiative?</p>"),
                    Div('knowledge_areas'),
                    css_class='col-md-6'),
                css_class='row',
            ),
            HTML("<p>12. Why did you choose to do this initiative? Based on a need?</p>"),
            Field('why_this_initiative', placeholder='not more than 5 sentences'),
            HTML("<p>13. How many direct beneficiaries will benefit from your planned initiative? (more than one option)</p>"),
            'number_of_beneficiaries',
            HTML("<p>14. Please select the age Groups of the beneficiaries</p>"),
            'age_of_beneficiaries',
            HTML("<p>15. Sex of beneficiaries</p>"),
            'sex_of_beneficiaries',
            HTML("<p>16. How many indirect beneficiaries will benefit from your planned initiative? (more than one option may apply)</p>"),
            'indirect_beneficiaries',
            HTML("<p>17. Are you planning to mobilize resources for this project?</p>"),
            'needs_resources',
            HTML("<p>17.a If so, from whom?</p>"),
            'resources_from',
            HTML("<p>18. What kind of support are you planning to receive? (you can select more than one option)</p>"),
            'resources_type',
            HTML("<p>19. Can you please tell us what your initiative is about, its objective and why is it important?</p>"),
            Field('description', placeholder='not more than 5 sentences'),
            HTML("<p>20. Can you please tell us your planned results?</p>"),
            Field('planned_results', placeholder='not more than 5 sentences'),
            HTML("<p>21. Can you please tell us your anticipated challenges?</p>"),
            Field('anticpated_challenges', placeholder='not more than 5 sentences'),
            HTML("<p>22. How are you planning to mitigate those challenges?</p>"),
            Field('mitigation_of_challenges', placeholder='not more than 5 sentences'),
            HTML("<p>24. Will the project be Sustainable? How will you ensure its sustainability?</p>"),
            Field('how_to_ensure_sustainability', placeholder='not more than 5 sentences'),
            FormActions(
                Submit('save', 'Save changes'),
                Button('cancel', 'Cancel')
            )
        )

    class Meta:
        model = YouthLedInitiative
        fields = '__all__'

