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
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.admin import site, ModelAdmin
from django import forms
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.contrib import messages
from django.utils.translation import ugettext as _t
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.widgets import FilteredSelectMultiple
from datetime import datetime
from collections import OrderedDict
from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Fieldset, Submit, Div, HTML, Layout

from referral_platform.locations.models import Location
from referral_platform.partners.models import Center
from referral_platform.registrations.models import Assessment, AssessmentSubmission, Registration
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
    member = forms.ModelMultipleChoiceField(queryset=Registration.objects.all(), widget=FilteredSelectMultiple("member", is_stacked=False))
    # id = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = YouthLedInitiative
        fields = '__all__'

    class Media:
        css = {'all': ('/static/admin/css/widgets.css',), }
        js = ('/admin/jsi18n/',)

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
            # self.fields['member'].queryset = Registration.objects.filter(partner_organization=self.request.user.partner)



        else:
            initials = kwargs.get('initial', '')

        partner_locations = initials['partner_locations'] if 'partner_locations' in initials else []
        partner_organization = initials['partner_organization'] if 'partner_organization' in initials else 0
        self.fields['location'].queryset = Location.objects.filter(parent__in=partner_locations)
        self.fields['member'].queryset = Registration.objects.filter(partner_organization=partner_organization)
        my_fields = OrderedDict()

        if not instance:
            my_fields['Search Youth'] = ['search_youth']

        self.helper = FormHelper()
        self.helper.form_show_labels = False
        # form_action = reverse('initiatives:add')
        # self.helper.layout = Layout()
        self.helper.layout = Layout(
            Div(
                Div('partner_organization', css_class='col-md-6', ),
                Div(PrependedText('title', _('Initiative Title')), css_class='col-md-6', ),
                css_class='row',
            ),
            # HTML(_('Please choose the members of this Initiative')),
            # 'members',
            HTML(_('Member')),
            'member',
            HTML(_('Location')),
            'location',

            HTML(_('Initiative Type')),
            'type',
            HTML(_('Duration')),
            'duration',)

        if instance:
            form_action = reverse('initiatives:edit', kwargs={'pk': instance.id})
            all_forms = Assessment.objects.filter( Q(partner=partner_organization) | Q(slug="init_registration")| Q(slug="init_exec"))
            new_forms = OrderedDict()

            registration_form = Assessment.objects.get(slug="init_registration")

            youth_registered = AssessmentSubmission.objects.filter(
                assessment_id=registration_form.id,
                registration_id=instance.id
            ).exists()

            for specific_form in all_forms:
                formtxt = '{assessment}?registry={registry}'.format(
                    assessment=reverse('initiatives:assessment', kwargs={'slug': specific_form.slug}),
                    registry=instance.id,
                )
                disabled = ""

                # if youth_registered:
                #     # if specific_form.slug == "registration":
                #     #     disabled = "disabled"
                #     # # check if the pre is already filled
                #     # else:
                #         order = 1  # int(specific_form.order.split(".")[1])
                #         if order == 1:
                #             # If the user filled the form disable it
                #             form_submitted = AssessmentSubmission.objects.filter(
                #                 assessment_id=specific_form.id, registration_id=instance.id).exists()
                #             if form_submitted:
                #                 disabled = "disabled"
                #         else:
                #             # make sure the user filled the form behind this one in order to enable it
                #             if previous_status == "disabled":
                #                 previous_submitted = AssessmentSubmission.objects.filter(
                #                     assessment_id=specific_form.id, registration_id=instance.id).exists()
                #                 if previous_submitted:
                #                     disabled = "disabled"
                #             else:
                #                 disabled = "disabled"
                # else:
                #     if specific_form.slug != "init_registration":
                #         disabled = "disabled"

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
                    test_html = test_html + '<div class="col-md-3"><a class="btn btn-success ' \
                                + new_forms[name][test_order]['disabled'] + '" href="' + new_forms[name][test_order][
                                    'form'] \
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

        # Rendering the assessments
        # if instance:
        #     form_action = reverse('initiatives:edit', kwargs={'pk': instance.id})
        #     all_forms = Assessment.objects.filter(Q(partner__isnull=True) | Q(partner=partner_organization))
        #     new_forms = OrderedDict()
        #
        #     registration_form = Assessment.objects.get(slug="registration")
        #
        #     youth_registered = AssessmentSubmission.objects.filter(
        #         assessment_id=registration_form.id,
        #         registration_id=instance.id
        #     ).exists()
        #
        #     for specific_form in all_forms:
        #         formtxt = '{assessment}?registry={registry}'.format(
        #             assessment=reverse('registrations:assessment', kwargs={'slug': specific_form.slug}),
        #             registry=instance.id,
        #         )
        #         disabled = ""
        #
        #         if youth_registered:
        #             if specific_form.slug == "registration":
        #                 disabled = "disabled"
        #             # check if the pre is already filled
        #             else:
        #                 order = 1  # int(specific_form.order.split(".")[1])
        #                 if order == 1:
        #                     # If the user filled the form disable it
        #                     form_submitted = AssessmentSubmission.objects.filter(
        #                         assessment_id=specific_form.id, registration_id=instance.id).exists()
        #                     if form_submitted:
        #                         disabled = "disabled"
        #                 else:
        #                     # make sure the user filled the form behind this one in order to enable it
        #                     if previous_status == "disabled":
        #                         previous_submitted = AssessmentSubmission.objects.filter(
        #                             assessment_id=specific_form.id, registration_id=instance.id).exists()
        #                         if previous_submitted:
        #                             disabled = "disabled"
        #                     else:
        #                         disabled = "disabled"
        #         else:
        #             if specific_form.slug != "registration":
        #                 disabled = "disabled"
        #
        #         if specific_form.name not in new_forms:
        #             new_forms[specific_form.name] = OrderedDict()
        #         new_forms[specific_form.name][specific_form.order] = {
        #             'title': specific_form.overview,
        #             'form': formtxt,
        #             'overview': specific_form.name,
        #             'disabled': disabled
        #         }
        #         previous_status = disabled
        #     assessment_fieldset = []
        #
        #     for name in new_forms:
        #         test_html = ""
        #
        #         for test_order in new_forms[name]:
        #             test_html = test_html + '<div class="col-md-3"><a class="btn btn-success ' \
        #                         + new_forms[name][test_order]['disabled'] + '" href="' + new_forms[name][test_order][
        #                             'form'] \
        #                         + '">' + new_forms[name][test_order][
        #                             'title'] + '</a></div> '
        #         assessment_div = Div(
        #             HTML(test_html),
        #             css_class='row'
        #         )
        #         test_fieldset = Fieldset(
        #             None,
        #             Div(
        #                 HTML('<h4 id="alternatives-to-hidden-labels">' + new_forms[name][test_order][
        #                     'overview'] + '</h4>')
        #             ),
        #             assessment_div,
        #             Div(
        #                 HTML('<div class="p-3"></div>'),
        #                 css_class='row'
        #             ),
        #             css_class='bd-callout bd-callout-warning'
        #         )
        #         assessment_fieldset.append(test_fieldset)
        #     for myflds in assessment_fieldset:
        #         self.helper.layout.append(myflds)

        self.helper.layout.append(
            FormActions(
                HTML('<a class="btn btn-info col-md-2" href="/initiatives/list/">' + _t('Cancel') + '</a>'),
                # Submit('save_add_another', _('Save and add another'), css_class='col-md-2'),
                Submit('save_and_continue', _('Save and continue'), css_class='col-md-2'),
                css_class='btn-actions'

            )
        )
        # self.helper.form_action = form_action
    # def clean(self):
    #
    #     cleaned_data = super(YouthLedInitiativePlanningForm, self).clean()
    #     youth_id = cleaned_data.get('youth_search_id')
    #     youth_id_edit = cleaned_data.get('youth_id')
    #     birthday_year = cleaned_data.get('youth_birthday_year')
    #     birthday_day = cleaned_data.get('youth_birthday_day')
    #     birthday_month = cleaned_data.get('youth_birthday_month')
    #     nationality = cleaned_data.get('youth_nationality')
    #     sex = cleaned_data.get('youth_sex')
    #     first_name = cleaned_data.get('youth_first_name')
    #     last_name = cleaned_data.get('youth_last_name')
    #     father_name = cleaned_data.get('youth_father_name')
    #     override_submit = cleaned_data.get('override_submit')
    #     form_str = '{} {} {}'.format(first_name, father_name, last_name)
    #     is_matching = False
    #     exists = False
    #     queryset = Registration.objects.all()
    #     continue_button = '<br/><button  class="btn btn-info" type="button" name="continue" value="continue" id="continue">Continue</button>'
    #
    #     if not override_submit:
    #         if youth_id:
    #             if queryset.filter(youth_id=youth_id, partner_organization=self.initial["partner"]).exists():
    #                 exists = True
    #
    #         if exists:
    #             raise forms.ValidationError(
    #                 "Youth is already registered with current partner"
    #             )
    #
    #         if self.instance.id:
    #             queryset = queryset.exclude(id=self.instance.id,
    #                                         partner_organization=self.instance.partner_organization)
    #
    #         filtered_results = queryset.filter(youth__birthday_year=birthday_year,
    #                                            youth__birthday_day=birthday_day,
    #                                            youth__birthday_month=birthday_month,
    #                                            youth__sex=sex)
    #         if not youth_id_edit:
    #             matching_results = ''
    #             for result in filtered_results:
    #                 result_str = '{} {} {}'.format(result.youth.first_name, result.youth.father_name,
    #                                                result.youth.last_name)
    #                 fuzzy_match = fuzz.ratio(form_str, result_str)
    #                 if fuzzy_match > 85:
    #                     matching_results = matching_results + "<a href='/initiatives/add/?youth_id=" + str(
    #                         result.youth_id) + "'>" + result_str + " - birthday:" + birthday_day + "/" + birthday_month + "/" + birthday_year + " - gender:" + sex + "</a><br/>"
    #                     is_matching = True
    #
    #             if is_matching:
    #                 raise forms.ValidationError(
    #                     mark_safe("Youth is already registered with another partner, "
    #                               "please check which one would you like to add:<br/>" + matching_results + "<br/> Or if new Youth click on continue:<br/>" + continue_button)
    #                 )

    def save(self, request=None, instance=None):
        instance = super(YouthLedInitiativePlanningForm, self).save()
        # instance = super(GradingTermForm, self).save()
        # instance.id = int(request.session.session_id)
        request.session['instance_id'] = instance.id
        # print('key is ' + instance.id)
        messages.success(request, _('Your data has been sent successfully to the server'))






