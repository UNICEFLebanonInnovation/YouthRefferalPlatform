from __future__ import unicode_literals, absolute_import, division

from django.utils.translation import ugettext as _
from django import forms
from django.core.urlresolvers import reverse

from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions, Accordion, PrependedText, InlineCheckboxes, InlineRadios
from crispy_forms.layout import Layout, Fieldset, Button, Submit, Div, Field, HTML

from .models import School


class ProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_show_labels = True
        self.helper.form_action = reverse('schools:profile', kwargs={})

        self.helper.layout = Layout(
            Fieldset(
                None,
                Div(
                    HTML('<h4 id="alternatives-to-hidden-labels">' + _('Current academic year') + '</h4>')
                ),
                Div(
                    HTML('<span class="badge badge-default">1</span>'),
                    Div('academic_year_start', css_class='col-md-3'),
                    HTML('<span class="badge badge-default">2</span>'),
                    Div('academic_year_end', css_class='col-md-3'),
                    HTML('<span class="badge badge-default">3</span>'),
                    Div('academic_year_exam_end', css_class='col-md-3'),
                    css_class='row',
                ),
                css_class='bd-callout bd-callout-warning'
            ),
            FormActions(
                Submit('save', _('Save')),
            )
        )

    def save(self, instance=None, request=None):
        instance = super(ProfileForm, self).save()

    class Meta:
        model = School
        fields = (
            'academic_year_start',
            'academic_year_end',
            'academic_year_exam_end',
        )
        initial_fields = fields
        widgets = {}

    class Media:
        js = ()
