from __future__ import unicode_literals, absolute_import, division

from django.utils.translation import ugettext as _
from django import forms
from django.core.urlresolvers import reverse

from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions, InlineRadios
from crispy_forms.layout import Layout, Fieldset, Button, Submit, Div, HTML

from referral_platform.youth.models import YoungPerson
from referral_platform.locations.models import Location
from .models import (
    Assessment
)

YES_NO_CHOICE = ((1, "Yes"), (0, "No"))

YEARS = list(((str(x), x) for x in range(1990, 2017)))
YEARS.append(('', _('---------')))

DAYS = list(((str(x), x) for x in range(1, 32)))
DAYS.append(('', _('---------')))


class CommonForm(forms.ModelForm):

    governorate = forms.ModelChoiceField(
        queryset=Location.objects.filter(parent__isnull=False), widget=forms.Select,
        empty_label=_('governorate'),
        required=False, to_field_name='id',
        initial=0
    )

    location = forms.ModelChoiceField(
        queryset=Location.objects.filter(parent__isnull=False), widget=forms.Select,
        empty_label=_('location'),
        required=False, to_field_name='id',
        initial=0
    )

    class Meta:
        model = YoungPerson
        fields = (
            'governorate',
            'location',
            'first_name',
            'father_name',
            'last_name',
            'sex',
            'birthday_year',
            'birthday_month',
            'birthday_day',
            'nationality',
            'address',
            'marital_status',
        )
        initial_fields = fields
        widgets = {}

    class Media:
        js = (
            'js/jquery-1.12.3.min.js',
            'js/jquery-ui-1.12.1.js',
            'js/validator.js',
            'js/registrations.js',
        )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(CommonForm, self).__init__(*args, **kwargs)

        instance = kwargs['instance'] if 'instance' in kwargs else ''
        form_action = reverse('youth:add')

        if instance:
            form_action = reverse('youth:edit', kwargs={'pk': instance.id})

            all_forms = Assessment.objects.all()
            dynamic_fields = []

            new_forms = {}

            for specific_form in all_forms:
                formtxt = '{assessment}?youth_id={youth_id}&status={status}'.format(
                    assessment=reverse('youth:assessment', kwargs={'slug': specific_form.slug}),
                    youth_id=instance.number,
                    status='registration',
                )
                if specific_form.name not in new_forms:
                    new_forms[specific_form.name] = {}

                new_forms[specific_form.name][specific_form.id] = {'title': specific_form.name,
                                                                           'form': formtxt,
                                                                           'overview': specific_form.overview}

            assessment_fieldset = []
            for name in new_forms:
                test_html = ""
                for test_order in new_forms[name]:
                    test_html = test_html + '<div class="col-md-3"><a class="btn btn-success" href="' + \
                                new_forms[name][test_order]['form'] + '">' + new_forms[name][test_order][
                                    'title'] + '</a></div> '

                assessment_div = Div(
                    HTML(test_html),
                    css_class='row'
                )
                testFieldset = Fieldset(
                    None,
                    Div(
                        HTML('<h4 id="alternatives-to-hidden-labels">' + new_forms[name][test_order]['overview'] + '</h4>')
                    ),
                    assessment_div,
                    Div(
                        HTML('<div class="p-3"></div>'),
                        css_class='row'
                    ),
                    css_class='bd-callout bd-callout-warning'
                )
                assessment_fieldset.append(testFieldset)

                dynamic_fields = assessment_fieldset


        self.helper = FormHelper()
        self.helper.form_show_labels = True
        self.helper.form_action = form_action
        self.helper.layout = Layout(

            Fieldset(
                None,
                Div(
                    HTML('<h4 id="alternatives-to-hidden-labels">Location Information</h4>')
                ),
                Div(
                    HTML('<span class="badge badge-default">2</span>'),
                    Div('governorate', css_class='col-md-3'),
                    css_class='row',
                ),
                Div(
                    HTML('<span class="badge badge-default">4</span>'),
                    Div('location', css_class='col-md-3'),
                    css_class='row',
                ),
                css_class='bd-callout bd-callout-warning'
            ),
            Fieldset(
                None,
                Div(
                    HTML('<h4 id="alternatives-to-hidden-labels">Personal Details</h4>')
                ),
                Div(
                    HTML('<span class="badge badge-default">2</span>'),
                    Div('first_name', css_class='col-md-3'),
                    HTML('<span class="badge badge-default">3</span>'),
                    Div('father_name', css_class='col-md-3'),
                    HTML('<span class="badge badge-default">4</span>'),
                    Div('last_name', css_class='col-md-3'),
                    css_class='row',
                ),
                Div(
                    HTML('<span class="badge badge-default">5</span>'),
                    Div('birthday_year', css_class='col-md-3'),
                    HTML('<span class="badge badge-default">6</span>'),
                    Div('birthday_month', css_class='col-md-3'),
                    HTML('<span class="badge badge-default">7</span>'),
                    Div('birthday_day', css_class='col-md-3'),
                    css_class='row',
                ),
                Div(
                    HTML('<span class="badge badge-default">8</span>'),
                    Div('sex', css_class='col-md-3'),
                    HTML('<span class="badge badge-default">9</span>'),
                    Div('nationality', css_class='col-md-3'),
                    HTML('<span class="badge badge-default">1</span>'),
                    Div('marital_status', css_class='col-md-3'),
                    css_class='row',
                ),
                Div(
                    HTML('<span class="badge badge-default">11</span>'),
                    Div('address', css_class='col-md-3'),
                    css_class='row',
                ),
                css_class='bd-callout bd-callout-warning'
            ),
        )

        if instance:
            for myflds in dynamic_fields:
                self.helper.layout.append(myflds)

        self.helper.layout.append(
            FormActions(
                Submit('save', _('Save')),
                Button('cancel', _('Cancel')),
                HTML('<a class="btn btn-info" href="/youth/">Back to list</a>'),
            )
        )


