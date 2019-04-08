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
from referral_platform.registrations.models import Assessment, Registration, AssessmentHash
from django.forms import SelectMultiple
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions, Accordion, PrependedText, InlineRadios, InlineField, Alert
from .models import YouthLedInitiative, YoungPerson, Location
from referral_platform.initiatives.models import AssessmentSubmission
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

YES_NO_CHOICE = ((False, _('No')), (True, _('Yes')))

allow_multiple_selected = True
class YouthLedInitiativePlanningForm(forms.ModelForm):
    OPTIONS = (
                ('basic services', _('Basic Services')),
                ('social Cohesion', _('Social cohesion')),
                ('environmental', _('Environmental')),
                ('health services', _('Health Services')),
                ('protection', _('Protection')),
                ('advocacy', _('Advocacy or Raising awareness')),
                ('political', _('Political')),
                ('religious and spiritual', _('Spiritual/Religious')),
                ('sports', _('Sports')),
                ('economic art cultural', _('Economic art cultural')),
                ('educational', _('educational')),
                ('other', _('Other'))
        )

    # Participants = forms.ModelMultipleChoiceField(queryset=Registration.objects.all(), widget=FilteredSelectMultiple("Participants", is_stacked=False))

    Participants = forms.ModelMultipleChoiceField(queryset=Registration.objects.all(), widget=FilteredSelectMultiple("Partcipants", is_stacked=False))

    type = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=OPTIONS)
    # id = forms.CharField(widget=forms.HiddenInput())
    search_youth = forms.CharField(
        label=_("Search Initiative"),
        widget=forms.TextInput,
        required=False
    )
    class Meta:
        model = YouthLedInitiative
        fields = '__all__'

    class Media:
        css = {'all': ('/admin/css/widgets.css', 'admin/css/overrides.css'), }
        js = ('/admin/jquery.js', '/admin/jsi18n/')


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

    # needs_resources = forms.ChoiceField(
    #     label=_("Needs Resources?"),
    #     widget=forms.Select, required=False,
    #     choices=(('True', _("Yes")), ('False', _("No"))),
    #     initial='no'
    # )

    def __init__(self, *args, **kwargs):
        super(YouthLedInitiativePlanningForm, self).__init__(*args, **kwargs)

        self.request = kwargs.pop('request', None)
        instance = kwargs.get('instance', '')
        if instance:
            initials = {}
            initials['partner_locations'] = instance.partner_organization.locations.all()
            self.fields['partner_organization'].widget.attrs['readonly'] = True
            # self.fields['Participants'].queryset = Registration.objects.filter(partner_organization=self.request.user.partner)



        else:
            initials = kwargs.get('initial', '')

        partner_locations = initials['partner_locations'] if 'partner_locations' in initials else []
        partner_organization = initials['partner_organization'] if 'partner_organization' in initials else 0
        self.fields['location'].queryset = Location.objects.filter(parent__in=partner_locations)
        # self.fields['Participants'].queryset = Registration.objects.filter(partner_organization=partner_organization)
        self.fields['Participants'].queryset = Registration.objects.filter(partner_organization=partner_organization)
        self.fields['partner_organization'].widget.attrs['readonly'] = True

        # self.fields['partner_organization'] = forms.CharField(disabled=True)
        # self.fields['partner_organization'] = forms.CharField(
        #     widget=forms.TextInput(attrs={'readonly': 'readonly'})
        # )
        my_fields = OrderedDict()

        if not instance:
            my_fields['Partner Information - please do not change'] = ['partner_organization']

        my_fields[_('Initiative Details')] = [
                                            'title',

                                            'duration',
                                            'location',
                                            # 'type',
                                            'Participants',
                                             ]

        self.helper = FormHelper()
        self.helper.form_show_labels = True
        # form_action = reverse('initiatives:add')
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

        # self.helper = FormHelper()
        # self.helper.layout = Layout(
        #     Row(
        #         Column('title', css_class='form-group col-md-6 mb-0'),
        #         Column('password', css_class='form-group col-md-6 mb-0'),
        #         css_class='form-row'
        #     ),
        #     'address_1',
        #     'address_2',
        #     Row(
        #         Column('duration', css_class='form-group col-md-6 mb-0'),
        #         Column('location', css_class='form-group col-md-4 mb-0'),
        #         Column('type', css_class='form-group col-md-2 mb-0'),
        #         css_class='form-row'
        #     ),
        #
        #
        # )
        #
        # self.helper = FormHelper()
        # self.helper.form_show_labels = False
        # # form_action = reverse('initiatives:add')
        # # self.helper.layout = Layout()
        # self.helper.layout = Layout(
        #     Div(
        #         Div('partner_organization', readonly=True),
        #
        #         Div(PrependedText('title', _('Initiative Title')),),
        #
        #     ),
        #     # HTML(_('Please choose the members of this Initiative')),
        #     # 'members',
        #     Div( HTML(_),
        #     'Participants',
        #     HTML(_('Location')),
        #     'location',
        #
        #     HTML(_('Initiative Type')),
        #     'type',
        #     HTML(_('Duration')),
        #     'duration',
        #
        # ))

        # Rendering the assessments
        if instance:
            form_action = reverse('initiatives:edit', kwargs={'pk': instance.id})
            # all_forms = Assessment.objects.filter(Q(slug="init_registration") | Q(slug="init_exec") | Q(slug='init_post_civic'))
            # all_forms = Assessment.objects.filter(Q(partner__isnull=True) | Q(partner=partner_organization))
            all_forms = Assessment.objects.filter(slug__in=["init_registration", "init_exec", "init_post_civic"])
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
                            if previous_status != "disabled":
                                previous_submitted = AssessmentSubmission.objects.filter(
                                    assessment_id=specific_form.id, initiative_id=instance.id).exists()
                                if previous_submitted:
                                    disabled = ""
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

        # self.helper.form_action = form_action
        self.helper.layout.append(
            FormActions(
                HTML('<a class="btn btn-info col-md-2" href="/initiatives/list/">' + _t('Cancel') + '</a>'),
                Submit('save_add_another', _('Save and add another'), css_class='col-md-2'),
                Submit('save_and_continue', _('Save and continue'), css_class='col-md-2'),
                Submit('save', _('Save'), css_class='col-md-2'),
                css_class='btn-actions'

            )
        )

    def clean_partner(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.partner_organization
        else:
            return self.cleaned_data['partner_organization']

    # def clean_foo_field(self):
    #     instance = getattr(self, 'instance', None)
    #     if instance and instance.id:
    #         return instance.YouthLedInitiativePlanningForm
    #     else:
    #         return self.cleaned_data['partner_organization']

    def save(self, request=None, instance=None):
        instance = super(YouthLedInitiativePlanningForm, self).save()
        # instance = super(GradingTermForm, self).save()
        # instance.id = int(request.session.session_id)
        request.session['instance_id'] = instance.id
        # print('key is ' + instance.id)
        messages.success(request, _('Your data has been sent successfully to the server'))







# from __future__ import unicode_literals, absolute_import, division
#
# from django.utils.translation import ugettext as _
# from django import forms
# from django.core.urlresolvers import reverse
# from django.db.models import Q
# from django.contrib import messages
# from django.utils.translation import ugettext as _t
# from django.utils.translation import ugettext_lazy as _
# from django.contrib.admin.widgets import FilteredSelectMultiple
# from collections import OrderedDict
# from crispy_forms.layout import Fieldset, Submit, Div, HTML, Layout
# from referral_platform.registrations.models import Assessment, Registration, AssessmentHash
# from crispy_forms.helper import FormHelper
# from crispy_forms.bootstrap import FormActions, Accordion, PrependedText, InlineRadios, InlineField, Alert
# from .models import YouthLedInitiative, YoungPerson, Location
# from referral_platform.initiatives.models import AssessmentSubmission
#
# YES_NO_CHOICE = ((False, _('No')), (True, _('Yes')))
#
#
# class YouthLedInitiativePlanningForm(forms.ModelForm):
#     # Participants = forms.ModelMultipleChoiceField(queryset=Registration.objects.all(), widget=FilteredSelectMultiple("Participants", is_stacked=False))
#     # search_youth = forms.CharField(
#     #     label=_("Search for youth by name"),
#     #     widget=forms.TextInput,
#     #     required=False
#     # )
#     # location = forms.CharField(
#     #     label=_("Location"),
#     #     widget=forms.TextInput,
#     #     required=False
#     # )
#     # duration = forms.CharField(
#     #     label=_("Duration"),
#     #     widget=forms.TextInput,
#     #     required=False
#     # )
#     # id = forms.CharField(widget=forms.HiddenInput())
#
#     class Meta:
#         model = YouthLedInitiative
#         fields = '__all__'
#
#     class Media:
#         css = {'all': ('/static/admin/css/widgets.css',), }
#         js = ('/admin/jsi18n/',)
#
#     # start_date = forms.DateField(
#     #     widget=DateTimePicker(
#     #         options={
#     #             "format": "mm/dd/yyyy",
#     #             "pickTime": False
#     #         }),
#     #     required=True
#     # )
#     #
#     # needs_resources = forms.TypedChoiceField(
#     #     coerce=lambda x: x == 'True',
#     #     choices=YES_NO_CHOICE,
#     #     widget=forms.RadioSelect
#     # )
#
#     needs_resources = forms.ChoiceField(
#         label=_("Needs Resources?"),
#         widget=forms.Select, required=False,
#         choices=(('True', _("Yes")), ('False', _("No"))),
#         initial='no'
#     )
#
#     def __init__(self, *args, **kwargs):
#         super(YouthLedInitiativePlanningForm, self).__init__(*args, **kwargs)
#
#         self.request = kwargs.pop('request', None)
#         instance = kwargs.get('instance', '')
#         if instance:
#             initials = {}
#             initials['partner_locations'] = instance.partner_organization.locations.all()
#             initials['partner_organization'] = instance.partner_organization
#             # self.fields['member'].queryset = Registration.objects.filter(partner_organization=self.request.user.partner)
#
#
#
#         else:
#             initials = kwargs.get('initial', '')
#
#         partner_locations = initials['partner_locations'] if 'partner_locations' in initials else []
#         partner_organization = initials['partner_organization'] if 'partner_organization' in initials else 0
#         self.fields['location'].queryset = Location.objects.filter(parent__in=partner_locations)
#         self.fields['Participants'].queryset = Registration.objects.filter(partner_organization=partner_organization)
#         self.fields['partner_organization'].widget.attrs['readonly'] = True
#         my_fields = OrderedDict()
#
#         if not instance:
#             my_fields['Search Youth'] = ['search_youth']
#
#
#
#         #     Div(
#         #         Div('partner_organization', readonly=True, css_class='col-md-4'),
#         #
#         #         Div(PrependedText('title', _('Initiative Title')), css_class='col-md-4'),
#         #
#         #     ),
#         #     # HTML(_('Please choose the members of this Initiative')),
#         #     # 'members',
#         #     HTML(_),
#         #     'Participants',
#         #     Div(HTML(_('Location')), 'location', css_class='col-md-3'),
#         #
#         #     Div(HTML(_('Initiative Type')), 'type', css_class='col-md-3'),
#         #     Div(HTML(_('Duration')), 'duration', css_class='col-md-3'),
#         #
#         # )
#
#         my_fields[_('Partner Organization')] = ['partner_organization']
#         my_fields[_('Initiative Title')] = ['title']
#         my_fields[_('Partcipants')] = ['participants']
#         my_fields[_('Initiative Information')] = ['location', 'dutation', 'type']
#
#         self.helper = FormHelper()
#         self.helper.form_show_labels = False
#         # form_action = reverse('initiatives:add')
#         # # self.helper.layout = Layout()
#         self.helper.layout = Layout()
#
#         for title in my_fields:
#             main_fieldset = Fieldset(None)
#             main_div = Div(css_class='row')
#
#             # Title Div
#             main_fieldset.fields.append(
#                 Div(
#                     HTML('<h4 id="alternatives-to-hidden-labels">' + _t(title) + '</h4>')
#                 )
#             )
#             # remaining fields, every 3 on a row
#             for myField in my_fields[title]:
#                 index = my_fields[title].index(myField) + 1
#                 main_div.append(
#                     HTML('<span class="badge badge-default">' + str(index) + '</span>'),
#                 )
#                 main_div.append(
#                     Div(myField, css_class='col-md-3'),
#                 )
#                 # to keep every 3 on a row, or the last field in the list
#                 if index % 3 == 0 or len(my_fields[title]) == index:
#                     main_fieldset.fields.append(main_div)
#                     main_div = Div(css_class='row')
#
#             main_fieldset.css_class = 'bd-callout bd-callout-warning'
#             self.helper.layout.append(main_fieldset)
#
#         # Rendering the assessments
#         if instance:
#             form_action = reverse('initiatives:edit', kwargs={'pk': instance.id})
#             all_forms = Assessment.objects.filter(Q(slug="init_registration") | Q(slug="init_exec"))
#             new_forms = OrderedDict()
#
#             registration_form = Assessment.objects.get(slug="init_registration")
#
#             youth_registered = AssessmentSubmission.objects.filter(
#                 assessment_id=registration_form.id,
#                 initiative_id=instance.id
#             ).exists()
#
#             for specific_form in all_forms:
#                 formtxt = '{assessment}?registry={registry}'.format(
#                     assessment=reverse('initiatives:assessment', kwargs={'slug': specific_form.slug}),
#                     registry=instance.id,
#                 )
#                 disabled = ""
#
#                 if youth_registered:
#                     if specific_form.slug == "init_registration":
#                         disabled = "disabled"
#                     # check if the pre is already filled
#                     else:
#                         order = 1  # int(specific_form.order.split(".")[1])
#                         if order == 1:
#                             # If the user filled the form disable it
#                             form_submitted = AssessmentSubmission.objects.filter(
#                                 assessment_id=specific_form.id, initiative_id=instance.id).exists()
#                             if form_submitted:
#                                 disabled = "disabled"
#                         else:
#                             # make sure the user filled the form behind this one in order to enable it
#                             if previous_status == "disabled":
#                                 previous_submitted = AssessmentSubmission.objects.filter(
#                                     assessment_id=specific_form.id, initiative_id=instance.id).exists()
#                                 if previous_submitted:
#                                     disabled = "disabled"
#                             else:
#                                 disabled = "disabled"
#                 else:
#                     if specific_form.slug != "init_registration":
#                         disabled = "disabled"
#
#                 if specific_form.name not in new_forms:
#                     new_forms[specific_form.name] = OrderedDict()
#                 new_forms[specific_form.name][specific_form.order] = {
#                     'title': specific_form.overview,
#                     'form': formtxt,
#                     'overview': specific_form.name,
#                     'disabled': disabled
#                 }
#                 previous_status = disabled
#             assessment_fieldset = []
#
#             for name in new_forms:
#                 test_html = ""
#
#                 for test_order in new_forms[name]:
#                     test_html = test_html + '<div class="col-md-3"><a class="btn btn-success ' \
#                                 + new_forms[name][test_order]['disabled'] + '" href="' + new_forms[name][test_order][
#                                     'form'] \
#                                 + '">' + new_forms[name][test_order][
#                                     'title'] + '</a></div> '
#                 assessment_div = Div(
#                     HTML(test_html),
#                     css_class='row'
#                 )
#                 test_fieldset = Fieldset(
#                     None,
#                     Div(
#                         HTML('<h4 id="alternatives-to-hidden-labels">' + new_forms[name][test_order][
#                             'overview'] + '</h4>')
#                     ),
#                     assessment_div,
#                     Div(
#                         HTML('<div class="p-3"></div>'),
#                         css_class='row'
#                     ),
#                     css_class='bd-callout bd-callout-warning'
#                 )
#                 assessment_fieldset.append(test_fieldset)
#                 for myflds in assessment_fieldset:
#                     self.helper.layout.append(myflds)
#         self.helper.layout.append(
#             FormActions(
#                 HTML('<a class="btn btn-info col-md-2" href="/initiatives/list/">' + _t('Cancel') + '</a>'),
#                 Submit('save_add_another', _('Save and add another'), css_class='col-md-2'),
#                 Submit('save_and_continue', _('Save and continue'), css_class='col-md-2'),
#                 Submit('save', _('Save'), css_class='col-md-2'),
#                 css_class='btn-actions'
#
#             )
#         )
#
#     def clean_foo_field(self):
#         instance = getattr(self, 'instance', None)
#         if instance and instance.id:
#             return instance.YouthLedInitiativePlanningForm
#         else:
#             return self.cleaned_data['partner_organization']
#
#     def save(self, request=None, instance=None):
#         instance = super(YouthLedInitiativePlanningForm, self).save()
#         # instance = super(GradingTermForm, self).save()
#         # instance.id = int(request.session.session_id)
#         request.session['instance_id'] = instance.id
#         # print('key is ' + instance.id)
#         messages.success(request, _('Your data has been sent successfully to the server'))
#
#
#
#
#
