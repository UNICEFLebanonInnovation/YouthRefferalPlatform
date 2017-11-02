from __future__ import unicode_literals, absolute_import, division

from collections import OrderedDict
from pprint import pprint

from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Fieldset, Submit, Div, HTML, Layout
from django import forms
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.utils.translation import ugettext as _, ugettext_lazy as __
from referral_platform.locations.models import Location
from referral_platform.partners.models import Center
from referral_platform.youth.models import YoungPerson
from .models import (
    Assessment,
    AssessmentSubmission)


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
            'trainer',
            'bayanati_ID',
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

        my_fields = OrderedDict()
        my_fields['Location Information'] = ['governorate', 'center', 'trainer', 'location']

        # Add Trainer name to Jordan
        jordan_location = Location.objects.get(name="Jordan")
        if jordan_location not in partner_locations:
            del self.fields['trainer']
            del self.fields['bayanati_ID']
            my_fields['Location Information'].remove('trainer')
        else:
            self.fields['bayanati_ID'].required = True
            self.fields['trainer'].required = True
            my_fields['Bayanati Information'] = ['bayanati_ID', ]

        # Add Centers for the partner having ones (For now only Jordan)
        if self.fields['center'].queryset.count() < 1:
            del self.fields['center']
            my_fields['Location Information'].remove('center')

        my_fields['Personal Details'] = ['first_name',
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

        for title in my_fields:
            main_fieldset = Fieldset(None)
            main_div = Div(css_class='row')

            # Title Div
            main_fieldset.fields.append(
                Div(
                    HTML('<h4 id="alternatives-to-hidden-labels">' + _(title) + '</h4>')
                )
            )
            # remaining fields, every 3 on a row
            for myField in my_fields[title]:
                index = my_fields[title].index(myField) + 1
                main_div.append(
                    HTML('<span class="badge badge-default">' + str(index) + '</span>'),
                )
                main_div.append(
                    Div(myField, css_class='col-md-3'),
                )
                # to keep every 3 on a row, or the last field in the list
                if index % 3 == 0 or len(my_fields[title]) == index:
                    main_fieldset.fields.append(main_div)
                    main_div = Div(css_class='row')

            main_fieldset.css_class = 'bd-callout bd-callout-warning'
            self.helper.layout.append(main_fieldset)

        # Rendering the assessments
        if instance:
            form_action = reverse('youth:edit', kwargs={'pk': instance.id})
            all_forms = Assessment.objects.filter(Q(partner__isnull=True) | Q(partner=partner))
            new_forms = OrderedDict()

            registration_form = Assessment.objects.get(slug="registration")

            youth_registered = AssessmentSubmission.objects.filter(
                Q(assessment_id=registration_form.id) & Q(youth_id=instance.id)
            ).exists()

            for specific_form in all_forms:
                formtxt = '{assessment}?youth_id={youth_id}&status={status}'.format(
                    assessment=reverse('youth:assessment', kwargs={'slug': specific_form.slug}),
                    youth_id=instance.number,
                    status='enrolled',
                )
                disabled = ""
                order = int(specific_form.order[specific_form.order.find("."):]) +1
                print(specific_form.slug)
                print(order)
                if youth_registered:
                    if specific_form.slug == "registration":
                        disabled = "disabled"
                    #check if the pre is already filled
                    else:
                        if order==1:
                            print("d1")
                            #If the user filled the form disable it
                            form_submitted = AssessmentSubmission.objects.filter(
                                assessment_id=specific_form.id, youth_id=instance.id).exists()
                            if form_submitted:
                                disabled = "disabled"
                                print("d2")
                        else:
                            #make sure the user filled the form behind this one in order to enable it
                            if previous_status == "disabled":
                                print("d3")
                                previous_submitted = AssessmentSubmission.objects.filter(
                                    assessment_id =specific_form.id, youth_id=instance.id).exists()
                                if previous_submitted:
                                    print("d4")
                                    disabled = "disabled"
                            else:
                                print("d5")
                                disabled = "disabled"
                else:
                    if specific_form.slug != "registration":
                        print("d6")
                        disabled = "disabled"

                if specific_form.name not in new_forms:
                    new_forms[specific_form.name] = OrderedDict()
                new_forms[specific_form.name][specific_form.order] = {
                    'title': specific_form.overview,
                    'form': formtxt,
                    'overview': specific_form.name,
                    'disabled': disabled
                }
                previous_status = disabled
            assessment_fieldset = []
            for name in new_forms:
                test_html = ""

                for test_order in new_forms[name]:
                    test_html = test_html + '<div class="col-md-3"><a class="btn btn-success '\
                                +new_forms[name][test_order]['disabled'] +'" href="' +new_forms[name][test_order]['form']\
                                + '">' + new_forms[name][test_order][
                                    'title'] + '</a></div> '
                assessment_div = Div(
                    HTML(test_html),
                    css_class='row'
                )
                test_fieldset = Fieldset(
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
                assessment_fieldset.append(test_fieldset)
            for myflds in assessment_fieldset:
                self.helper.layout.append(myflds)

        self.helper.form_action = form_action

        self.helper.layout.append(
            FormActions(
                Submit('save', _('Save')),
                HTML('<a class="btn btn-info" href="/youth/">' + _('Cancel') + '</a>'),
            )
        )
