

from __future__ import unicode_literals, absolute_import, division

from django.utils.translation import ugettext as _
from django import forms
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.contrib import messages
from django.utils.translation import ugettext as _t
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.widgets import FilteredSelectMultiple
from collections import OrderedDict
from crispy_forms.layout import Fieldset, Submit, Div, HTML, Layout
from referral_platform.registrations.models import Assessment, Registration
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions, Accordion, PrependedText, InlineRadios, InlineField, Alert
from .models import YouthLedInitiative
from referral_platform.locations.models import Location
from referral_platform.initiatives.models import AssessmentSubmission

YES_NO_CHOICE = ((False, _('No')), (True, _('Yes')))


class YouthLedInitiativePlanningForm(forms.ModelForm):
    Participants = forms.ModelMultipleChoiceField(queryset=Registration.objects.none(),
                                                  widget=FilteredSelectMultiple("Participants", is_stacked=False))
    search_youth = forms.CharField(
        label=_("Search for youth by name or id"),
        widget=forms.TextInput,
        required=False
    )

    governorate = forms.ModelChoiceField(
        label=_('Governorate'),
        queryset=Location.objects.filter(parent__isnull=False), widget=forms.Select,
        required=True, to_field_name='id',
    )


    class Meta:
        model = YouthLedInitiative
        fields = '__all__'

    # class Media:
    #     # css = {'all': ('/static/admin/css/widgets.css',), }
    #     js = ('/admin/jsi18n/',)

    def __init__(self, *args, **kwargs):
        super(YouthLedInitiativePlanningForm, self).__init__(*args, **kwargs)

        self.request = kwargs.pop('request', None)
        instance = kwargs.get('instance', '')
        if instance:
            initials = {}
            initials['partner_locations'] = instance.partner_organization.locations.all()
            initials['partner_organization'] = instance.partner_organization
        else:
            initials = kwargs.get('initial', '')

        partner_locations = initials['partner_locations'] if 'partner_locations' in initials else []
        partner_organization = initials['partner_organization'] if 'partner_organization' in initials else 0
        self.fields['governorate'].queryset = Location.objects.filter(parent__in=partner_locations)
        self.fields['Participants'].queryset = Registration.objects.filter(partner_organization=partner_organization)
        self.fields['partner_organization'].widget.attrs['readonly'] = True
        my_fields = OrderedDict()

        if not instance:
            my_fields['Search Youth'] = ['partner_organization', 'title']

        # my_fields[_('Partner Organization')] = ['partner_organization']
        # my_fields[_('Initiative Title')] = ['title']
        my_fields[_('Participants')] = ['Participants']
        my_fields[_('Initiative Information')] = ['governorate', 'duration', 'type']

        self.helper = FormHelper()
        self.helper.form_show_labels = True
        # form_action = reverse('initiatives:add')
        # # self.helper.layout = Layout()
        self.helper.layout = Layout()

        for title in my_fields:
            main_fieldset = Fieldset(None)
            main_div = Div(css_class='row')

            # Title Div
            main_fieldset.fields.append(
                Div(
                    HTML('<h4 id="alternatives-to-hidden-labels">' + _t(title) + '</h4>')
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
            form_action = reverse('initiatives:edit', kwargs={'pk': instance.id})
            all_forms = Assessment.objects.filter(Q(slug="init_registration") | Q(slug="init_exec"))
            new_forms = OrderedDict()

            registration_form = Assessment.objects.get(slug="init_registration")

            youth_registered = AssessmentSubmission.objects.filter(
                assessment_id=registration_form.id,
                initiative_id=instance.id
            ).exists()

            for specific_form in all_forms:
                formtxt = '{assessment}?registry={registry}'.format(
                    assessment=reverse('initiatives:assessment', kwargs={'slug': specific_form.slug}),
                    registry=instance.id,
                )
                disabled = ""

                if youth_registered:
                    if specific_form.slug == "init_registration":
                        disabled = "disabled"
                    # check if the pre is already filled
                    else:
                        order = 1  # int(specific_form.order.split(".")[1])
                        if order == 1:
                            # If the user filled the form disable it
                            form_submitted = AssessmentSubmission.objects.filter(
                                assessment_id=specific_form.id, initiative_id=instance.id).exists()
                            if form_submitted:
                                disabled = "disabled"
                        else:
                            # make sure the user filled the form behind this one in order to enable it
                            if previous_status == "disabled":
                                previous_submitted = AssessmentSubmission.objects.filter(
                                    assessment_id=specific_form.id, initiative_id=instance.id).exists()
                                if previous_submitted:
                                    disabled = "disabled"
                            else:
                                disabled = "disabled"
                else:
                    if specific_form.slug != "init_registration":
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
        self.helper.layout.append(
            FormActions(
                HTML('<a class="btn btn-info col-md-2" href="/initiatives/list/">' + _t('Cancel') + '</a>'),
                Submit('save_add_another', _('Save and add another'), css_class='col-md-2'),
                Submit('save_and_continue', _('Save and continue'), css_class='col-md-2'),
                Submit('save', _('Save'), css_class='col-md-2'),
                css_class='btn-actions'
            )
        )

    def clean_foo_field(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            return instance.YouthLedInitiativePlanningForm
        else:
            return self.cleaned_data['partner_organization']

    def save(self, request=None, instance=None):
        instance = super(YouthLedInitiativePlanningForm, self).save()
        request.session['instance_id'] = instance.id
        messages.success(request, _('Your data has been sent successfully to the server'))


