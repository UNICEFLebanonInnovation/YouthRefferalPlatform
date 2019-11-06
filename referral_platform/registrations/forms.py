from __future__ import unicode_literals, absolute_import, division

from django import forms
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.contrib import messages
from django.utils.translation import ugettext as _t
from django.utils.translation import ugettext_lazy as _

from datetime import datetime
from collections import OrderedDict
from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Fieldset, Submit, Div, HTML, Layout

from referral_platform.locations.models import Location
from referral_platform.partners.models import Center
from referral_platform.registrations.models import Assessment, AssessmentSubmission
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

from referral_platform.youth.models import YoungPerson, Nationality, Center
from .serializers import RegistrationSerializer
from .models import Registration
from django.utils.safestring import mark_safe

current_year = datetime.today().year

YEARS = list(((str(x), x) for x in range(current_year - 26, current_year - 6)))
YEARS.insert(0, ('', '---------'))

DAYS = list(((str(x), x) for x in range(1, 32)))
DAYS.insert(0, ('', '---------'))


class CommonForm(forms.ModelForm):

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
    location = forms.CharField(
        label=_("Location"),
        widget=forms.TextInput,
        required=False
    )
    center = forms.ModelChoiceField(
        label=_('Center'),
        queryset=Center.objects.all(), widget=forms.Select,
        empty_label=_('Center'),
        required=True, to_field_name='id',
    )
    youth_id = forms.IntegerField(
        widget=forms.HiddenInput,
        required=False
    )
    override_submit = forms.IntegerField(
        widget=forms.HiddenInput,
        required=False
    )
    youth_bayanati_ID = forms.CharField(
        label=_('Bayanati ID'),
        widget=forms.TextInput, required=False
    )
    youth_first_name = forms.CharField(
        label=_("First name"),
        widget=forms.TextInput, required=True
    )
    youth_father_name = forms.CharField(
        label=_("Father name"),
        widget=forms.TextInput, required=True
    )
    youth_last_name = forms.CharField(
        label=_("Last name"),
        widget=forms.TextInput, required=True
    )
    youth_sex = forms.ChoiceField(
        label=_("Gender"),
        widget=forms.Select, required=True,
        choices=(
            ('', '----------'),
            ('male', _('Male')),
            ('female', _('Female')),
        )
    )
    youth_birthday_year = forms.ChoiceField(
        label=_("Birthday year"),
        widget=forms.Select, required=True,
        choices=YEARS
    )
    youth_birthday_month = forms.ChoiceField(
        label=_("Birthday month"),
        widget=forms.Select, required=True,
        choices=(
            ('', '----------'),
            ('1', _('January')),
            ('2', _('February')),
            ('3', _('March')),
            ('4', _('April')),
            ('5', _('May')),
            ('6', _('June')),
            ('7', _('July')),
            ('8', _('August')),
            ('9', _('September')),
            ('10', _('October')),
            ('11', _('November')),
            ('12', _('December')),
        )
    )
    youth_birthday_day = forms.ChoiceField(
        label=_("Birthday day"),
        widget=forms.Select, required=True,
        choices=DAYS
    )
    youth_nationality = forms.ModelChoiceField(
        label=_("Nationality"),
        queryset=Nationality.objects.all(), widget=forms.Select,
        required=True, to_field_name='id',
    )
    youth_address = forms.CharField(
        label=_("Address"),
        widget=forms.Textarea, required=False,
    )
    youth_marital_status = forms.ChoiceField(
        label=_('Marital status'),
        widget=forms.Select,
        choices=(
            ('married', _('Married')),
            ('engaged', _('Engaged')),
            ('divorced', _('Divorced')),
            ('widower', _('Widower')),
            ('single', _('Single')),
        ),
        required=True, initial='single'
    )

    class Meta:
        model = Registration
        fields = (
            'governorate',
            'location',
            'center',
            'trainer',
            'youth_bayanati_ID',
            'youth_id',
            'youth_first_name',
            'youth_father_name',
            'youth_last_name',
            'youth_sex',
            'youth_birthday_year',
            'youth_birthday_month',
            'youth_birthday_day',
            'youth_nationality',
            'youth_address',
            'youth_marital_status',
            'override_submit',
            'comments',
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
        if instance:
            initials = {}
            initials['partner_locations'] = instance.partner_organization.locations.all()
            initials['partner'] = instance.partner_organization

        else:
            initials = kwargs.get('initial', '')

        partner_locations = initials['partner_locations'] if 'partner_locations' in initials else []
        partner = initials['partner'] if 'partner' in initials else 0
        self.fields['governorate'].queryset = Location.objects.filter(parent__in=partner_locations)
        self.fields['center'].queryset = Center.objects.filter(partner_organization=partner)
        my_fields = OrderedDict()

        if not instance:
            my_fields['Search Youth'] = ['search_youth']

        my_fields[_('Location Information')] = ['governorate', 'center', 'trainer', 'location']

        # Add Trainer name to Jordan
        jordan_location = Location.objects.get(name_en="Jordan")
        if jordan_location not in partner_locations:
            del self.fields['trainer']
            del self.fields['youth_bayanati_ID']
            my_fields[_('Location Information')].remove('trainer')
        else:
            self.fields['youth_bayanati_ID'].required = True
            self.fields['trainer'].required = True
            my_fields['Bayanati'] = ['youth_bayanati_ID', ]

        # Add Centers for the partner having ones (For now only Jordan)
        if self.fields['center'].queryset.count() < 1:
            del self.fields['center']
            my_fields[_('Location Information')].remove('center')

        my_fields[_('Personal Details')] = ['youth_first_name',
                                            'youth_father_name',
                                            'youth_last_name',
                                            'youth_birthday_day',
                                            'youth_birthday_month',
                                            'youth_birthday_year',
                                            'youth_sex',
                                            'youth_nationality',
                                            'youth_marital_status',
                                            'youth_address',
                                            'comments', ]

        self.helper = FormHelper()
        self.helper.form_show_labels = True
        form_action = reverse('registrations:add')
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
            form_action = reverse('registrations:edit', kwargs={'pk': instance.id})
            all_forms = Assessment.objects.filter(Q(partner__isnull=True) | Q(partner=partner))

            new_forms = OrderedDict()
            m1 = Assessment.objects.filter(Q(slug="init_registration") | Q(slug="init_exec"))
            xforms = list(all_forms)
            removed = list(m1)
            for x in removed:
                xforms.remove(x)
            all_form = tuple(xforms)

            registration_form = Assessment.objects.get(slug="registration")
            previous_status = "disabled"
            youth_registered = AssessmentSubmission.objects.filter(
                assessment_id=registration_form.id,
                registration_id=instance.id
            ).exists()

            for specific_form in all_form:
                formtxt = '{assessment}?registry={registry}'.format(
                    assessment=reverse('registrations:assessment', kwargs={'slug': specific_form.slug}),
                    registry=instance.id,
                )
                disabled = ""
                order = specific_form.order
                if youth_registered:
                    if specific_form.slug == "registration":
                        disabled = "disabled"
                    # check if the pre is already filled
                    else:
                        # order = 1  # int(specific_form.order.split(".")[1])
                        if order == 1:
                            # If the user filled the form disable it
                            form_submitted = AssessmentSubmission.objects.filter(
                                assessment_id=specific_form.id, registration_id=instance.id).exists()
                            if form_submitted:
                                disabled = "disabled"

                        else:
                            # # make sure the user filled the form behind this one in order to enable it

                            if previous_status == "disabled":
                                previous_submitted = AssessmentSubmission.objects.filter(
                                        assessment_id=specific_form.id, registration_id=instance.id).exists()
                                if previous_submitted:
                                    disabled = "disabled"
                            else:
                                    disabled = "disabled"
                            if specific_form.slug == "post_assessment":
                                if AssessmentSubmission.objects.filter(assessment_id=2.1, registration_id=instance.id).exists():
                                    disabled = ""
                                else:
                                    disabled = "disabled"

                            if specific_form.slug == "post_entrepreneurship":
                                if AssessmentSubmission.objects.filter(assessment_id=3.1, registration_id=instance.id).exists():
                                    disabled = ""
                                else:
                                    disabled = "disabled"



                else:
                    if specific_form.slug != "registration":
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
                                + new_forms[name][test_order]['disabled'] + '" href="' + \
                                new_forms[name][test_order][
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

        self.helper.form_action = form_action

        self.helper.layout.append(
            FormActions(
                HTML('<a class="btn btn-info col-md-2" href="/registrations/list/">' + _t('Cancel') + '</a>'),
                Submit('save_add_another', _('Save and add another'), css_class='col-md-2'),
                Submit('save_and_continue', _('Save and continue'), css_class='col-md-2'),
                Submit('save', _('Save'), css_class='col-md-2'),
                css_class='btn-actions'

                )
            )

    def clean(self):

        cleaned_data = super(CommonForm, self).clean()
        youth_id = cleaned_data.get('youth_search_id')
        youth_id_edit = cleaned_data.get('youth_id')
        birthday_year = cleaned_data.get('youth_birthday_year')
        birthday_day = cleaned_data.get('youth_birthday_day')
        birthday_month = cleaned_data.get('youth_birthday_month')
        nationality = cleaned_data.get('youth_nationality')
        sex = cleaned_data.get('youth_sex')
        first_name = cleaned_data.get('youth_first_name')
        last_name = cleaned_data.get('youth_last_name')
        father_name = cleaned_data.get('youth_father_name')
        override_submit = cleaned_data.get('override_submit')
        form_str = '{} {} {}'.format(first_name, father_name, last_name)
        is_matching = False
        exists = False
        queryset = Registration.objects.all()
        continue_button = '<br/><button  class="btn btn-info" type="button" name="continue" value="continue" id="continue">Continue</button>'

        if not override_submit:
            if youth_id:
                if queryset.filter(youth_id=youth_id, partner_organization=self.initial["partner"]).exists():
                    exists = True

            if exists:
                raise forms.ValidationError(
                    "Youth is already registered with current partner"
                )

            if self.instance.id:
                queryset = queryset.exclude(id=self.instance.id, partner_organization=self.instance.partner_organization)

            filtered_results = queryset.filter(youth__birthday_year=birthday_year,
                                                   youth__birthday_day=birthday_day,
                                                   youth__birthday_month=birthday_month,
                                                   youth__sex=sex)
            if not youth_id_edit:
                matching_results = ''
                for result in filtered_results:
                    result_str = '{} {} {}'.format(result.youth.first_name, result.youth.father_name, result.youth.last_name)
                    fuzzy_match = fuzz.ratio(form_str, result_str)
                    if fuzzy_match > 85:
                        matching_results = matching_results + "<a href='/registrations/add/?youth_id="+str(result.youth_id)+"'>"+result_str+" - birthday:"+birthday_day+"/"+birthday_month+"/"+birthday_year+" - gender:"+sex+"</a><br/>"
                        is_matching = True

                if is_matching:
                    raise forms.ValidationError(
                        mark_safe("Youth is already registered with another partner, "
                                  "please check which one would you like to add:<br/>"+matching_results+"<br/> Or if new Youth click on continue:<br/>"+continue_button)
                        )

    def save(self, request=None, instance=None):
        if instance:
            serializer = RegistrationSerializer(instance, data=request.POST)
            if serializer.is_valid():
                serializer.update(validated_data=serializer.validated_data, instance=instance)
                request.session['instance_id'] = instance.id
                messages.success(request, _('Your data has been sent successfully to the server'))

            else:
                messages.warning(request, serializer.errors)
        else:
            serializer = RegistrationSerializer(data=request.POST)
            if serializer.is_valid():
                instance = serializer.create(validated_data=serializer.validated_data)
                instance.owner = request.user
                instance.modified_by = request.user
                instance.partner_organization = request.user.partner
                instance.save()
                request.session['instance_id'] = instance.id
                messages.success(request, _('Your data has been sent successfully to the server'))
            else:
                messages.warning(request, serializer.errors)


class BeneficiaryCommonForm(CommonForm):

        class Meta:
            model = Registration
            fields = (
                'governorate',
                'location',
                'center',
                'trainer',
                'youth_bayanati_ID',
                'youth_id',
                'youth_first_name',
                'youth_father_name',
                'youth_last_name',
                'youth_sex',
                'youth_birthday_year',
                'youth_birthday_month',
                'youth_birthday_day',
                'youth_nationality',
                'youth_address',
                'youth_marital_status',
                'override_submit',
                'comments',
            )
            initial_fields = fields
            widgets = {}

        class Media:
            js = (

            )

        def __init__(self, *args, **kwargs):

            self.request = kwargs.pop('request', None)
            super(BeneficiaryCommonForm, self).__init__(*args, **kwargs)
            instance = kwargs.get('instance', '')
            if instance:
                initials = {}
                initials['partner_locations'] = instance.partner_organization.locations.all()
                initials['partner'] = instance.partner_organization

            else:
                initials = kwargs.get('initial', '')

            partner_locations = initials['partner_locations'] if 'partner_locations' in initials else []
            partner = initials['partner'] if 'partner' in initials else 0
            self.fields['governorate'].queryset = Location.objects.filter(parent__in=partner_locations)
            self.fields['center'].queryset = Center.objects.filter(partner_organization=partner)
            my_fields = OrderedDict()

            if not instance:
                my_fields['Search Youth'] = ['search_youth']

            my_fields[_('Location Information')] = ['governorate', 'center', 'trainer', 'location']

            # Add Trainer name to Jordan
            jordan_location = Location.objects.get(name_en="Jordan")
            if jordan_location not in partner_locations:
                # del self.fields['trainer']
                # del self.fields['youth_bayanati_ID']
                my_fields[_('Location Information')].remove('trainer')
            else:
                self.fields['youth_bayanati_ID'].required = True
                self.fields['trainer'].required = True
                my_fields['Bayanati'] = ['youth_bayanati_ID', ]

            # Add Centers for the partner having ones (For now only Jordan)
            if self.fields['center'].queryset.count() < 1:
                del self.fields['center']
                my_fields[_('Location Information')].remove('center')

            my_fields[_('Personal Details')] = ['youth_first_name',
                                                'youth_father_name',
                                                'youth_last_name',
                                                'youth_birthday_day',
                                                'youth_birthday_month',
                                                'youth_birthday_year',
                                                'youth_sex',
                                                'youth_nationality',
                                                'youth_marital_status',
                                                'youth_address',
                                                'comments', ]

            self.helper = FormHelper()
            self.helper.form_show_labels = True
            form_action = reverse('registrations:add')
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
                form_action = reverse('registrations:edit', kwargs={'pk': instance.id})
                all_forms = Assessment.objects.filter(Q(partner__isnull=True) | Q(partner=partner))
                new_forms = OrderedDict()

                registration_form = Assessment.objects.get(slug="registration")

                youth_registered = AssessmentSubmission.objects.filter(
                    assessment_id=registration_form.id,
                    registration_id=instance.id
                ).exists()

                for specific_form in all_forms:
                    formtxt = '{assessment}?registry={registry}'.format(
                        assessment=reverse('registrations:assessment', kwargs={'slug': specific_form.slug}),
                        registry=instance.id,
                    )
                    disabled = ""

                    if youth_registered:
                        if specific_form.slug == "registration":
                            disabled = "disabled"
                        # check if the pre is already filled
                        else:
                            order = 1  # int(specific_form.order.split(".")[1])
                            if order == 1:
                                # If the user filled the form disable it
                                form_submitted = AssessmentSubmission.objects.filter(
                                    assessment_id=specific_form.id, registration_id=instance.id).exists()
                                if form_submitted:
                                    disabled = "disabled"
                            else:
                                # make sure the user filled the form behind this one in order to enable it
                                if previous_status == "disabled":
                                    previous_submitted = AssessmentSubmission.objects.filter(
                                        assessment_id=specific_form.id, registration_id=instance.id).exists()
                                    if previous_submitted:
                                        disabled = "disabled"
                                else:
                                    disabled = "disabled"
                    else:
                        if specific_form.slug != "registration":
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
                                    + new_forms[name][test_order]['disabled'] + '" href="' + \
                                    new_forms[name][test_order][
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

            self.helper.form_action = form_action

            self.helper.layout.append(
                FormActions(
                    HTML('<a class="btn btn-info col-md-2" href="/registrations/list/">' + _t('Cancel') + '</a>'),
                    Submit('save_and_continue', _('Save and continue'), css_class='col-md-2'),
                    css_class='btn-actions'

                    )
                )




# from __future__ import unicode_literals, absolute_import, division
#
# from django import forms
# from django.core.urlresolvers import reverse
# from django.db.models import Q
# from django.contrib import messages
# from django.utils.translation import ugettext as _t
# from django.utils.translation import ugettext_lazy as _
#
# from datetime import datetime
# from collections import OrderedDict
# from crispy_forms.bootstrap import FormActions
# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Fieldset, Submit, Div, HTML, Layout
#
# from referral_platform.locations.models import Location
# from referral_platform.partners.models import Center
# from referral_platform.registrations.models import Assessment, AssessmentSubmission
# from fuzzywuzzy import fuzz
# from fuzzywuzzy import process
#
# from referral_platform.youth.models import YoungPerson, Nationality, Center
# from .serializers import RegistrationSerializer
# from .models import Registration
# from django.utils.safestring import mark_safe
#
# current_year = datetime.today().year
#
# YEARS = list(((str(x), x) for x in range(current_year - 26, current_year - 6)))
# YEARS.insert(0, ('', '---------'))
#
# DAYS = list(((str(x), x) for x in range(1, 32)))
# DAYS.insert(0, ('', '---------'))
#
#
# class CommonForm(forms.ModelForm):
#
#     search_youth = forms.CharField(
#         label=_("Search for youth by name or id"),
#         widget=forms.TextInput,
#         required=False
#     )
#     governorate = forms.ModelChoiceField(
#         label=_('Governorate'),
#         queryset=Location.objects.filter(parent__isnull=False), widget=forms.Select,
#         required=True, to_field_name='id',
#     )
#     location = forms.CharField(
#         label=_("Location"),
#         widget=forms.TextInput,
#         required=False
#     )
#     center = forms.ModelChoiceField(
#         label=_('Center'),
#         queryset=Center.objects.all(), widget=forms.Select,
#         empty_label=_('Center'),
#         required=True, to_field_name='id',
#     )
#     youth_id = forms.IntegerField(
#         widget=forms.HiddenInput,
#         required=False
#     )
#     override_submit = forms.IntegerField(
#         widget=forms.HiddenInput,
#         required=False
#     )
#     youth_bayanati_ID = forms.CharField(
#         label=_('Bayanati ID'),
#         widget=forms.TextInput, required=False
#     )
#     youth_first_name = forms.CharField(
#         label=_("First name"),
#         widget=forms.TextInput, required=True
#     )
#     youth_father_name = forms.CharField(
#         label=_("Father name"),
#         widget=forms.TextInput, required=True
#     )
#     youth_last_name = forms.CharField(
#         label=_("Last name"),
#         widget=forms.TextInput, required=True
#     )
#     youth_sex = forms.ChoiceField(
#         label=_("Gender"),
#         widget=forms.Select, required=True,
#         choices=(
#             ('', '----------'),
#             ('male', _('Male')),
#             ('female', _('Female')),
#         )
#     )
#     youth_birthday_year = forms.ChoiceField(
#         label=_("Birthday year"),
#         widget=forms.Select, required=True,
#         choices=YEARS
#     )
#     youth_birthday_month = forms.ChoiceField(
#         label=_("Birthday month"),
#         widget=forms.Select, required=True,
#         choices=(
#             ('', '----------'),
#             ('1', _('January')),
#             ('2', _('February')),
#             ('3', _('March')),
#             ('4', _('April')),
#             ('5', _('May')),
#             ('6', _('June')),
#             ('7', _('July')),
#             ('8', _('August')),
#             ('9', _('September')),
#             ('10', _('October')),
#             ('11', _('November')),
#             ('12', _('December')),
#         )
#     )
#     youth_birthday_day = forms.ChoiceField(
#         label=_("Birthday day"),
#         widget=forms.Select, required=True,
#         choices=DAYS
#     )
#     youth_nationality = forms.ModelChoiceField(
#         label=_("Nationality"),
#         queryset=Nationality.objects.all(), widget=forms.Select,
#         required=True, to_field_name='id',
#     )
#     youth_address = forms.CharField(
#         label=_("Address"),
#         widget=forms.Textarea, required=False,
#     )
#     youth_marital_status = forms.ChoiceField(
#         label=_('Marital status'),
#         widget=forms.Select,
#         choices=(
#             ('married', _('Married')),
#             ('engaged', _('Engaged')),
#             ('divorced', _('Divorced')),
#             ('widower', _('Widower')),
#             ('single', _('Single')),
#         ),
#         required=True, initial='single'
#     )
#
#     class Meta:
#         model = Registration
#         fields = (
#             'governorate',
#             'location',
#             'center',
#             'trainer',
#             'youth_bayanati_ID',
#             'youth_id',
#             'youth_first_name',
#             'youth_father_name',
#             'youth_last_name',
#             'youth_sex',
#             'youth_birthday_year',
#             'youth_birthday_month',
#             'youth_birthday_day',
#             'youth_nationality',
#             'youth_address',
#             'youth_marital_status',
#             'override_submit',
#             'comments',
#         )
#         initial_fields = fields
#         widgets = {}
#
#     class Media:
#         js = (
#
#         )
#
#     def __init__(self, *args, **kwargs):
#
#         self.request = kwargs.pop('request', None)
#         super(CommonForm, self).__init__(*args, **kwargs)
#         instance = kwargs.get('instance', '')
#         if instance:
#             initials = {}
#             initials['partner_locations'] = instance.partner_organization.locations.all()
#             initials['partner'] = instance.partner_organization
#
#         else:
#             initials = kwargs.get('initial', '')
#
#         partner_locations = initials['partner_locations'] if 'partner_locations' in initials else []
#         partner = initials['partner'] if 'partner' in initials else 0
#         self.fields['governorate'].queryset = Location.objects.filter(parent__in=partner_locations)
#         self.fields['center'].queryset = Center.objects.filter(partner_organization=partner)
#         my_fields = OrderedDict()
#
#         if not instance:
#             my_fields['Search Youth'] = ['search_youth']
#
#         my_fields[_('Location Information')] = ['governorate', 'center', 'trainer', 'location']
#
#         # Add Trainer name to Jordan
#         jordan_location = Location.objects.get(name_en="Jordan")
#         if jordan_location not in partner_locations:
#             del self.fields['trainer']
#             del self.fields['youth_bayanati_ID']
#             my_fields[_('Location Information')].remove('trainer')
#         else:
#             self.fields['youth_bayanati_ID'].required = True
#             self.fields['trainer'].required = True
#             my_fields['Bayanati'] = ['youth_bayanati_ID', ]
#
#         # Add Centers for the partner having ones (For now only Jordan)
#         if self.fields['center'].queryset.count() < 1:
#             del self.fields['center']
#             my_fields[_('Location Information')].remove('center')
#
#         my_fields[_('Personal Details')] = ['youth_first_name',
#                                             'youth_father_name',
#                                             'youth_last_name',
#                                             'youth_birthday_day',
#                                             'youth_birthday_month',
#                                             'youth_birthday_year',
#                                             'youth_sex',
#                                             'youth_nationality',
#                                             'youth_marital_status',
#                                             'youth_address',
#                                             'comments', ]
#
#         self.helper = FormHelper()
#         self.helper.form_show_labels = True
#         form_action = reverse('registrations:add')
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
#             form_action = reverse('registrations:edit', kwargs={'pk': instance.id})
#             all_forms = Assessment.objects.filter(Q(partner__isnull=True) | Q(partner=partner))
#             new_forms = OrderedDict()
#             m1 = Assessment.objects.filter(Q(slug="init_registration") | Q(slug="init_exec"))
#             xforms = list(all_forms)
#             removed = list(m1)
#             for x in removed:
#                 xforms.remove(x)
#             all_form = tuple(xforms)
#
#             registration_form = Assessment.objects.get(slug="registration")
#
#             youth_registered = AssessmentSubmission.objects.filter(
#                 assessment_id=registration_form.id,
#                 registration_id=instance.id
#             ).exists()
#
#             for specific_form in all_form:
#                 formtxt = '{assessment}?registry={registry}'.format(
#                     assessment=reverse('registrations:assessment', kwargs={'slug': specific_form.slug}),
#                     registry=instance.id,
#                 )
#                 disabled = ""
#
#                 if youth_registered:
#                     if specific_form.slug == "registration":
#                         disabled = "disabled"
#                     # check if the pre is already filled
#                     else:
#                         order = 1  # int(specific_form.order.split(".")[1])
#                         if order == 1:
#                             # If the user filled the form disable it
#                             form_submitted = AssessmentSubmission.objects.filter(
#                                 assessment_id=specific_form.id, registration_id=instance.id).exists()
#                             if form_submitted:
#                                 disabled = "disabled"
#                         else:
#                             # make sure the user filled the form behind this one in order to enable it
#                             if previous_status == "disabled":
#                                 previous_submitted = AssessmentSubmission.objects.filter(
#                                     assessment_id=specific_form.id, registration_id=instance.id).exists()
#                                 if previous_submitted:
#                                     disabled = "disabled"
#                             else:
#                                 disabled = "disabled"
#                 else:
#                     if specific_form.slug != "registration":
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
#             for myflds in assessment_fieldset:
#                 self.helper.layout.append(myflds)
#
#         self.helper.form_action = form_action
#
#         self.helper.layout.append(
#             FormActions(
#                 HTML('<a class="btn btn-info col-md-2" href="/registrations/list/">' + _t('Cancel') + '</a>'),
#                 Submit('save_add_another', _('Save and add another'), css_class='col-md-2'),
#                 Submit('save_and_continue', _('Save and continue'), css_class='col-md-2'),
#                 Submit('save', _('Save'), css_class='col-md-2'),
#                 css_class='btn-actions'
#
#                 )
#             )
#
#     def clean(self):
#
#         cleaned_data = super(CommonForm, self).clean()
#         youth_id = cleaned_data.get('youth_search_id')
#         youth_id_edit = cleaned_data.get('youth_id')
#         birthday_year = cleaned_data.get('youth_birthday_year')
#         birthday_day = cleaned_data.get('youth_birthday_day')
#         birthday_month = cleaned_data.get('youth_birthday_month')
#         nationality = cleaned_data.get('youth_nationality')
#         sex = cleaned_data.get('youth_sex')
#         first_name = cleaned_data.get('youth_first_name')
#         last_name = cleaned_data.get('youth_last_name')
#         father_name = cleaned_data.get('youth_father_name')
#         override_submit = cleaned_data.get('override_submit')
#         form_str = '{} {} {}'.format(first_name, father_name, last_name)
#         is_matching = False
#         exists = False
#         queryset = Registration.objects.all()
#         continue_button = '<br/><button  class="btn btn-info" type="button" name="continue" value="continue" id="continue">Continue</button>'
#
#         if not override_submit:
#             if youth_id:
#                 if queryset.filter(youth_id=youth_id, partner_organization=self.initial["partner"]).exists():
#                     exists = True
#
#             if exists:
#                 raise forms.ValidationError(
#                     "Youth is already registered with current partner"
#                 )
#
#             if self.instance.id:
#                 queryset = queryset.exclude(id=self.instance.id, partner_organization=self.instance.partner_organization)
#
#             filtered_results = queryset.filter(youth__birthday_year=birthday_year,
#                                                    youth__birthday_day=birthday_day,
#                                                    youth__birthday_month=birthday_month,
#                                                    youth__sex=sex)
#             if not youth_id_edit:
#                 matching_results = ''
#                 for result in filtered_results:
#                     result_str = '{} {} {}'.format(result.youth.first_name, result.youth.father_name, result.youth.last_name)
#                     fuzzy_match = fuzz.ratio(form_str, result_str)
#                     if fuzzy_match > 85:
#                         matching_results = matching_results + "<a href='/registrations/add/?youth_id="+str(result.youth_id)+"'>"+result_str+" - birthday:"+birthday_day+"/"+birthday_month+"/"+birthday_year+" - gender:"+sex+"</a><br/>"
#                         is_matching = True
#
#                 if is_matching:
#                     raise forms.ValidationError(
#                         mark_safe("Youth is already registered with another partner, "
#                                   "please check which one would you like to add:<br/>"+matching_results+"<br/> Or if new Youth click on continue:<br/>"+continue_button)
#                         )
#
#     def save(self, request=None, instance=None):
#         if instance:
#             serializer = RegistrationSerializer(instance, data=request.POST)
#             if serializer.is_valid():
#                 serializer.update(validated_data=serializer.validated_data, instance=instance)
#                 request.session['instance_id'] = instance.id
#                 messages.success(request, _('Your data has been sent successfully to the server'))
#
#             else:
#                 messages.warning(request, serializer.errors)
#         else:
#             serializer = RegistrationSerializer(data=request.POST)
#             if serializer.is_valid():
#                 instance = serializer.create(validated_data=serializer.validated_data)
#                 instance.owner = request.user
#                 instance.modified_by = request.user
#                 instance.partner_organization = request.user.partner
#                 instance.save()
#                 request.session['instance_id'] = instance.id
#                 messages.success(request, _('Your data has been sent successfully to the server'))
#             else:
#                 messages.warning(request, serializer.errors)
#
#
# class BeneficiaryCommonForm(CommonForm):
#
#         class Meta:
#             model = Registration
#             fields = (
#                 'governorate',
#                 'location',
#                 'center',
#                 'trainer',
#                 'youth_bayanati_ID',
#                 'youth_id',
#                 'youth_first_name',
#                 'youth_father_name',
#                 'youth_last_name',
#                 'youth_sex',
#                 'youth_birthday_year',
#                 'youth_birthday_month',
#                 'youth_birthday_day',
#                 'youth_nationality',
#                 'youth_address',
#                 'youth_marital_status',
#                 'override_submit',
#                 'comments',
#             )
#             initial_fields = fields
#             widgets = {}
#
#         class Media:
#             js = (
#
#             )
#
#         def __init__(self, *args, **kwargs):
#
#             self.request = kwargs.pop('request', None)
#             super(BeneficiaryCommonForm, self).__init__(*args, **kwargs)
#             instance = kwargs.get('instance', '')
#             if instance:
#                 initials = {}
#                 initials['partner_locations'] = instance.partner_organization.locations.all()
#                 initials['partner'] = instance.partner_organization
#
#             else:
#                 initials = kwargs.get('initial', '')
#
#             partner_locations = initials['partner_locations'] if 'partner_locations' in initials else []
#             partner = initials['partner'] if 'partner' in initials else 0
#             self.fields['governorate'].queryset = Location.objects.filter(parent__in=partner_locations)
#             self.fields['center'].queryset = Center.objects.filter(partner_organization=partner)
#             my_fields = OrderedDict()
#
#             if not instance:
#                 my_fields['Search Youth'] = ['search_youth']
#
#             my_fields[_('Location Information')] = ['governorate', 'center', 'trainer', 'location']
#
#             # Add Trainer name to Jordan
#             jordan_location = Location.objects.get(name_en="Jordan")
#             if jordan_location not in partner_locations:
#                 # del self.fields['trainer']
#                 # del self.fields['youth_bayanati_ID']
#                 my_fields[_('Location Information')].remove('trainer')
#             else:
#                 self.fields['youth_bayanati_ID'].required = True
#                 self.fields['trainer'].required = True
#                 my_fields['Bayanati'] = ['youth_bayanati_ID', ]
#
#             # Add Centers for the partner having ones (For now only Jordan)
#             if self.fields['center'].queryset.count() < 1:
#                 del self.fields['center']
#                 my_fields[_('Location Information')].remove('center')
#
#             my_fields[_('Personal Details')] = ['youth_first_name',
#                                                 'youth_father_name',
#                                                 'youth_last_name',
#                                                 'youth_birthday_day',
#                                                 'youth_birthday_month',
#                                                 'youth_birthday_year',
#                                                 'youth_sex',
#                                                 'youth_nationality',
#                                                 'youth_marital_status',
#                                                 'youth_address',
#                                                 'comments', ]
#
#             self.helper = FormHelper()
#             self.helper.form_show_labels = True
#             form_action = reverse('registrations:add')
#             self.helper.layout = Layout()
#
#             for title in my_fields:
#                 main_fieldset = Fieldset(None)
#                 main_div = Div(css_class='row')
#
#                 # Title Div
#                 main_fieldset.fields.append(
#                     Div(
#                         HTML('<h4 id="alternatives-to-hidden-labels">' + _t(title) + '</h4>')
#                     )
#                 )
#                 # remaining fields, every 3 on a row
#                 for myField in my_fields[title]:
#                     index = my_fields[title].index(myField) + 1
#                     main_div.append(
#                         HTML('<span class="badge badge-default">' + str(index) + '</span>'),
#                     )
#                     main_div.append(
#                         Div(myField, css_class='col-md-3'),
#                     )
#                     # to keep every 3 on a row, or the last field in the list
#                     if index % 3 == 0 or len(my_fields[title]) == index:
#                         main_fieldset.fields.append(main_div)
#                         main_div = Div(css_class='row')
#
#                 main_fieldset.css_class = 'bd-callout bd-callout-warning'
#                 self.helper.layout.append(main_fieldset)
#
#             # Rendering the assessments
#             if instance:
#                 form_action = reverse('registrations:edit', kwargs={'pk': instance.id})
#                 all_forms = Assessment.objects.filter(Q(partner__isnull=True) | Q(partner=partner))
#                 new_forms = OrderedDict()
#                 m1 = Assessment.objects.filter(Q(slug="init_registration") | Q(slug="init_exec"))
#                 xforms = list(all_forms)
#                 removed = list(m1)
#                 for x in removed:
#                     xforms.remove(x)
#                 all_form = tuple(xforms)
#                 registration_form = Assessment.objects.get(slug="registration")
#
#                 youth_registered = AssessmentSubmission.objects.filter(
#                     assessment_id=registration_form.id,
#                     registration_id=instance.id
#                 ).exists()
#
#                 for specific_form in all_form:
#                     formtxt = '{assessment}?registry={registry}'.format(
#                         assessment=reverse('registrations:assessment', kwargs={'slug': specific_form.slug}),
#                         registry=instance.id,
#                     )
#                     disabled = ""
#
#                     if youth_registered:
#                         if specific_form.slug == "registration":
#                             disabled = "disabled"
#                         # check if the pre is already filled
#                         else:
#                             order = 1  # int(specific_form.order.split(".")[1])
#                             if order == 1:
#                                 # If the user filled the form disable it
#                                 form_submitted = AssessmentSubmission.objects.filter(
#                                     assessment_id=specific_form.id, registration_id=instance.id).exists()
#                                 if form_submitted:
#                                     disabled = "disabled"
#                             else:
#                                 # make sure the user filled the form behind this one in order to enable it
#                                 if previous_status == "disabled":
#                                     previous_submitted = AssessmentSubmission.objects.filter(
#                                         assessment_id=specific_form.id, registration_id=instance.id).exists()
#                                     if previous_submitted:
#                                         disabled = "disabled"
#                                 else:
#                                     disabled = "disabled"
#                     else:
#                         if specific_form.slug != "registration":
#                             disabled = "disabled"
#
#                     if specific_form.name not in new_forms:
#                         new_forms[specific_form.name] = OrderedDict()
#                     new_forms[specific_form.name][specific_form.order] = {
#                         'title': specific_form.overview,
#                         'form': formtxt,
#                         'overview': specific_form.name,
#                         'disabled': disabled
#                     }
#                     previous_status = disabled
#                 assessment_fieldset = []
#
#                 for name in new_forms:
#                     test_html = ""
#
#                     for test_order in new_forms[name]:
#                         test_html = test_html + '<div class="col-md-3"><a class="btn btn-success ' \
#                                     + new_forms[name][test_order]['disabled'] + '" href="' + \
#                                     new_forms[name][test_order][
#                                         'form'] \
#                                     + '">' + new_forms[name][test_order][
#                                         'title'] + '</a></div> '
#                     assessment_div = Div(
#                         HTML(test_html),
#                         css_class='row'
#                     )
#                     test_fieldset = Fieldset(
#                         None,
#                         Div(
#                             HTML('<h4 id="alternatives-to-hidden-labels">' + new_forms[name][test_order][
#                                 'overview'] + '</h4>')
#                         ),
#                         assessment_div,
#                         Div(
#                             HTML('<div class="p-3"></div>'),
#                             css_class='row'
#                         ),
#                         css_class='bd-callout bd-callout-warning'
#                     )
#                     assessment_fieldset.append(test_fieldset)
#                 for myflds in assessment_fieldset:
#                     self.helper.layout.append(myflds)
#
#             self.helper.form_action = form_action
#
#             self.helper.layout.append(
#                 FormActions(
#                     HTML('<a class="btn btn-info col-md-2" href="/registrations/list/">' + _t('Cancel') + '</a>'),
#                     Submit('save_and_continue', _('Save and continue'), css_class='col-md-2'),
#                     css_class='btn-actions'
#
#                     )
#                 )
#
#
