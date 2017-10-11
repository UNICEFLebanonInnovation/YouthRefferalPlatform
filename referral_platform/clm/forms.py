from __future__ import unicode_literals, absolute_import, division

from collections import OrderedDict

from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy as __
from django import forms
from django.core.urlresolvers import reverse
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import Layout, Fieldset, Submit, Div, HTML

from referral_platform.partners.models import Center
from referral_platform.youth.models import YoungPerson
from referral_platform.locations.models import Location
from .models import (
    Assessment
)


class CommonForm(forms.ModelForm):
    governorate = forms.ModelChoiceField(
        queryset=Location.objects.filter(parent__isnull=False), widget=forms.Select,
        empty_label=__('governorate'),
        required=True, to_field_name='id',
    )
    center = forms.ModelChoiceField(
        queryset=Center.objects.all(), widget=forms.Select,
        empty_label=__('center'),
        required=True, to_field_name='id',
    )

    class Meta:
        model = YoungPerson
        fields = (
            'governorate',
            'location',
            'center',
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
        )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(CommonForm, self).__init__(*args, **kwargs)

        instance = kwargs.get('instance', '')
        initials = kwargs.get('initial', '')
        partner_locations = initials['partner_locations'] if 'partner_locations' in initials else ''
        partner = initials['partner'] if 'partner' in initials else ''
        self.fields['governorate'].queryset = Location.objects.filter(parent__in=partner_locations)
        self.fields['center'].queryset = Center.objects.filter(partner_organization=partner)

        myFields = OrderedDict()
        myFields['Location Information'] = ['governorate', 'center', 'location']
        if self.fields['center'].queryset.count() <1:
            del self.fields['center']
            myFields['Location Information'].remove('center')

        myFields['Personal Details'] = ['first_name',
                                        'father_name',
                                        'last_name',
                                        'birthday_day',
                                        'birthday_month',
                                        'birthday_year',
                                        'sex',
                                        'nationality',
                                        'marital_status',
                                        'address', ]

        self.helper = FormHelper()
        self.helper.form_show_labels = True
        form_action = reverse('youth:add')
        self.helper.layout = Layout()

        for title in myFields:
            maindFieldset = Fieldset(None)
            mainDiv = Div(css_class='row')

            # Title Div
            print title
            maindFieldset.fields.append(
                Div(
                    HTML('<h4 id="alternatives-to-hidden-labels">' + _(title) + '</h4>')
                )
            )
            # remaining fields, every 3 on a row
            for myField in myFields[title]:
                index = myFields[title].index(myField) + 1
                mainDiv.append(
                    HTML('<span class="badge badge-default">' + str(index) + '</span>'),
                )
                mainDiv.append(
                    Div(myField, css_class='col-md-3'),
                )
                # to keep every 3 on a row, or the last field in the list
                if index % 3 == 0 or len(myFields[title]) == index:
                    maindFieldset.fields.append(mainDiv)
                    mainDiv = Div(css_class='row')

            maindFieldset.css_class = 'bd-callout bd-callout-warning'
            self.helper.layout.append(maindFieldset)

        #Rendering the assessments
        if instance:
            form_action = reverse('youth:edit', kwargs={'pk': instance.id})
            all_forms = Assessment.objects.all()
            new_forms = OrderedDict()

            for specific_form in all_forms:
                formtxt = '{assessment}?youth_id={youth_id}&status={status}'.format(
                    assessment=reverse('youth:assessment', kwargs={'slug': specific_form.slug}),
                    youth_id=instance.number,
                    status='registration',
                )
                if specific_form.name not in new_forms:
                    new_forms[specific_form.name] = OrderedDict()
                new_forms[specific_form.name][specific_form.order] = {
                    'title': specific_form.overview,
                    'form': formtxt,
                    'overview': specific_form.name
                }
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
                        HTML('<h4 id="alternatives-to-hidden-labels">' + new_forms[name][test_order][
                            'overview'] + '</h4>')
                    ),
                    assessment_div,
                    Div(
                        HTML('<div class="p-3"></div>'),
                        css_class='row'
                    ),
                    css_class='bd-callout bd-callout-warning'
                )
                assessment_fieldset.append(testFieldset)
            for myflds in assessment_fieldset:
                self.helper.layout.append(myflds)

        self.helper.form_action = form_action

        self.helper.layout.append(
            FormActions(
                Submit('save', _('Save')),
                HTML('<a class="btn btn-info" href="/youth/">' + _('Cancel') + '</a>'),
            )
        )
