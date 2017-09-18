from __future__ import unicode_literals, absolute_import, division

from django.utils.translation import ugettext as _
from django import forms
from django.core.urlresolvers import reverse

from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions, InlineRadios
from crispy_forms.layout import Layout, Fieldset, Button, Submit, Div, HTML

from referral_platform.youth.models import YoungPerson
from referral_platform.students.models import (
    Student,
    Nationality,
)
from referral_platform.schools.models import (
    School,
    EducationalLevel,
)
from referral_platform.locations.models import Location
from .models import (
    CLM,
    BLN,
    RS,
    CBECE,
    Cycle,
    RSCycle,
    Disability,
    Site,
    Assessment
)
from .serializers import BLNSerializer

YES_NO_CHOICE = ((1, "Yes"), (0, "No"))

YEARS = list(((str(x), x) for x in range(1990, 2017)))
YEARS.append(('', _('---------')))

DAYS = list(((str(x), x) for x in range(1, 32)))
DAYS.append(('', _('---------')))


class CommonForm(forms.ModelForm):

    new_registry = forms.TypedChoiceField(
        label=_("First time registered?"),
        choices=YES_NO_CHOICE,
        coerce=lambda x: bool(int(x)),
        widget=forms.RadioSelect,
        required=True,
    )
    student_outreached = forms.TypedChoiceField(
        label=_("Student outreached?"),
        choices=YES_NO_CHOICE,
        coerce=lambda x: bool(int(x)),
        widget=forms.RadioSelect,
        required=True,
    )
    have_barcode = forms.TypedChoiceField(
        label=_("Have barcode with him?"),
        choices=YES_NO_CHOICE,
        coerce=lambda x: bool(int(x)),
        widget=forms.RadioSelect,
        required=False,
    )
    search_barcode = forms.CharField(widget=forms.TextInput, required=False)
    # search_student = forms.CharField(widget=forms.TextInput, required=False)
    outreach_barcode = forms.CharField(widget=forms.TextInput, required=False)

    governorate = forms.ModelChoiceField(
        queryset=Location.objects.filter(parent__isnull=True), widget=forms.Select,
        empty_label=_('Governorate'),
        required=True, to_field_name='id',
        initial=0
    )
    district = forms.ModelChoiceField(
        queryset=Location.objects.filter(parent__isnull=False), widget=forms.Select,
        empty_label=_('District'),
        required=True, to_field_name='id',
        initial=0
    )
    location = forms.CharField(widget=forms.TextInput, required=True)
    language = forms.MultipleChoiceField(
        choices=CLM.LANGUAGES,
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    student_first_name = forms.CharField(widget=forms.TextInput, required=True)
    student_father_name = forms.CharField(widget=forms.TextInput, required=True)
    student_last_name = forms.CharField(widget=forms.TextInput, required=True)
    student_sex = forms.ChoiceField(
        widget=forms.Select, required=True,
        choices=YoungPerson.GENDER
    )
    student_birthday_year = forms.ChoiceField(
        widget=forms.Select, required=True,
        choices=YEARS
    )
    student_birthday_month = forms.ChoiceField(
        widget=forms.Select, required=True,
        choices=YoungPerson.MONTHS
    )
    student_birthday_day = forms.ChoiceField(
        widget=forms.Select, required=True,
        choices=DAYS
    )

    student_nationality = forms.ModelChoiceField(
        queryset=Nationality.objects.all(), widget=forms.Select,
        empty_label=_('Student nationality'),
        required=True, to_field_name='id',
    )

    student_mother_fullname = forms.CharField(widget=forms.TextInput, required=True)
    student_address = forms.CharField(widget=forms.TextInput, required=True)
    student_p_code = forms.CharField(widget=forms.TextInput, required=False)

    disability = forms.ModelChoiceField(
        queryset=Disability.objects.all(), widget=forms.Select,
        empty_label=_('Disability'),
        required=True, to_field_name='id',
        initial=1
    )
    student_family_status = forms.ChoiceField(
        widget=forms.Select, required=True,
        choices=YoungPerson.FAMILY_STATUS,
        initial='single'
    )
    student_have_children = forms.TypedChoiceField(
        label=_("Have children?"),
        choices=YES_NO_CHOICE,
        coerce=lambda x: bool(int(x)),
        widget=forms.RadioSelect,
        required=False,
    )

    have_labour = forms.MultipleChoiceField(
        choices=CLM.HAVE_LABOUR,
        widget=forms.CheckboxSelectMultiple,
        required=False, initial='no'
    )
    labours = forms.MultipleChoiceField(
        choices=CLM.LABOURS,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    labour_hours = forms.CharField(widget=forms.TextInput, required=False)
    hh_educational_level = forms.ModelChoiceField(
        queryset=EducationalLevel.objects.all(), widget=forms.Select,
        empty_label=_('HH educational level'),
        required=False, to_field_name='id',
    )

    student_id = forms.CharField(widget=forms.HiddenInput, required=False)
    enrollment_id = forms.CharField(widget=forms.HiddenInput, required=False)
    student_outreach_child = forms.CharField(widget=forms.HiddenInput, required=False)

    participation = forms.ChoiceField(
        widget=forms.Select, required=False,
        choices=CLM.PARTICIPATION
    )
    barriers = forms.MultipleChoiceField(
        choices=CLM.BARRIERS,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    learning_result = forms.ChoiceField(
        widget=forms.Select, required=False,
        choices=CLM.LEARNING_RESULT
    )

    def __init__(self, *args, **kwargs):
        super(CommonForm, self).__init__(*args, **kwargs)

        self.fields['cycle'].empty_label = _('-----------')
        self.fields['governorate'].empty_label = _('-----------')
        self.fields['district'].empty_label = _('-----------')
        self.fields['student_sex'].empty_label = _('-----------')
        self.fields['student_nationality'].empty_label = _('-----------')
        self.fields['disability'].empty_label = _('-----------')
        self.fields['hh_educational_level'].empty_label = _('-----------')

    def save(self, request=None, instance=None, serializer=None):
        if instance:
            serializer = serializer(instance, data=request.POST)
            if serializer.is_valid():
                serializer.update(validated_data=serializer.validated_data, instance=instance)
        else:
            serializer = serializer(data=request.POST)
            if serializer.is_valid():
                instance = serializer.create(validated_data=serializer.validated_data)
                instance.owner = request.user
                instance.save()
            else:
                return False

        return True

    class Meta:
        model = CLM
        fields = (
            'outreach_barcode',
            'governorate',
            'district',
            'location',
            'language',
            'student_first_name',
            'student_father_name',
            'student_last_name',
            'student_sex',
            'student_birthday_year',
            'student_birthday_month',
            'student_birthday_day',
            'student_nationality',
            'student_mother_fullname',
            'student_address',
            'student_p_code',
            'disability',
            'student_family_status',
            'student_have_children',
            'have_labour',
            'labours',
            'labour_hours',
            'hh_educational_level',
            'participation',
            'barriers',
            'learning_result',
            'student_id',
            'enrollment_id',
            'student_outreach_child',
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


class BLNForm(CommonForm):

    cycle = forms.ModelChoiceField(
        queryset=Cycle.objects.all(), widget=forms.Select,
        empty_label=_('Programme Cycle'),
        required=True, to_field_name='id',
        initial=0
    )
    referral = forms.MultipleChoiceField(
        choices=CLM.REFERRAL,
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(BLNForm, self).__init__(*args, **kwargs)

        pre_test = ''
        post_test = ''
        display_assessment = ' d-none'
        display_registry = ''
        instance = kwargs['instance'] if 'instance' in kwargs else ''
        form_action = reverse('youth:bln_add')

        if instance:
            form_action = reverse('youth:bln_edit', kwargs={'pk': instance.id})
            assessment_pre = Assessment.objects.get(slug='bln_pre_test')
            assessment_post = Assessment.objects.get(slug='bln_post_test')
            display_assessment = ''
            display_registry = ' d-none'
            pre_test = '{form}?d[status]={status}&returnURL={callback}'.format(
                form=assessment_pre.assessment_form,
                status='pre_test',
                callback=self.request.build_absolute_uri(
                    reverse('youth:bln_assessment', kwargs={'pk': instance.id})
                )
            )
            post_test = '{form}?d[status]={status}&returnURL={callback}'.format(
                form=assessment_post.assessment_form,
                status='post_test',
                callback=self.request.build_absolute_uri(
                    reverse('youth:bln_assessment', kwargs={'pk': instance.id})
                )
            )

        self.helper = FormHelper()
        self.helper.form_show_labels = True
        self.helper.form_action = form_action
        self.helper.layout = Layout(
            Fieldset(
                None,
                Div(
                    HTML('<h4 id="alternatives-to-hidden-labels">Registry</h4>')
                ),
                Div(
                    'student_id',
                    'enrollment_id',
                    'student_outreach_child',
                    HTML('<span class="badge badge-default">1</span>'),
                    Div(InlineRadios('new_registry'), css_class='col-md-3'),
                    HTML('<span class="badge badge-default">2</span>'),
                    Div(InlineRadios('student_outreached'), css_class='col-md-3'),
                    HTML('<span class="badge badge-default">3</span>'),
                    Div(InlineRadios('have_barcode'), css_class='col-md-3'),
                    css_class='row',
                ),
                css_class='bd-callout bd-callout-warning'+display_registry
            ),
            Fieldset(
                None,
                Div(
                    HTML('<h4 id="alternatives-to-hidden-labels">Register by Barcode</h4>')
                ),
                Div(
                    Div('search_barcode', css_class='col-md-6'),
                    css_class='row',
                ),
                css_id='register_by_barcode', css_class='bd-callout bd-callout-warning'+display_registry
            ),
            # Fieldset(
            #     None,
            #     Div(
            #         HTML('<h4 id="alternatives-to-hidden-labels">Search old student</h4>')
            #     ),
            #     Div(
            #         Div('search_student', css_class='col-md-6'),
            #         css_class='row',
            #     ),
            #     css_id='search_options', css_class='bd-callout bd-callout-warning'+display_registry
            # ),
            Fieldset(
                None,
                Div(
                    HTML('<h4 id="alternatives-to-hidden-labels">Program Information</h4>')
                ),
                Div(
                    HTML('<span class="badge badge-default">1</span>'),
                    Div('cycle', css_class='col-md-3'),
                    HTML('<span class="badge badge-default">2</span>'),
                    Div('governorate', css_class='col-md-3'),
                    HTML('<span class="badge badge-default">3</span>'),
                    Div('district', css_class='col-md-3'),
                    css_class='row',
                ),
                Div(
                    HTML('<span class="badge badge-default">4</span>'),
                    Div('location', css_class='col-md-3'),
                    HTML('<span class="badge badge-default">5</span>'),
                    Div('language', css_class='col-md-3'),
                    css_class='row',
                ),
                css_class='bd-callout bd-callout-warning'
            ),
            Fieldset(
                None,
                Div(
                    HTML('<h4 id="alternatives-to-hidden-labels">Child Information</h4>')
                ),
                Div(
                    HTML('<span class="badge badge-default">1</span>'),
                    Div('referral', css_class='col-md-9'),
                    css_class='row',
                ),
                Div(
                    HTML('<span class="badge badge-default">2</span>'),
                    Div('student_first_name', css_class='col-md-3'),
                    HTML('<span class="badge badge-default">3</span>'),
                    Div('student_father_name', css_class='col-md-3'),
                    HTML('<span class="badge badge-default">4</span>'),
                    Div('student_last_name', css_class='col-md-3'),
                    css_class='row',
                ),
                Div(
                    HTML('<span class="badge badge-default">5</span>'),
                    Div('student_birthday_year', css_class='col-md-3'),
                    HTML('<span class="badge badge-default">6</span>'),
                    Div('student_birthday_month', css_class='col-md-3'),
                    HTML('<span class="badge badge-default">7</span>'),
                    Div('student_birthday_day', css_class='col-md-3'),
                    css_class='row',
                ),
                Div(
                    HTML('<span class="badge badge-default">8</span>'),
                    Div('student_sex', css_class='col-md-3'),
                    HTML('<span class="badge badge-default">9</span>'),
                    Div('student_nationality', css_class='col-md-3'),
                    HTML('<span class="badge badge-default">10</span>'),
                    Div('student_mother_fullname', css_class='col-md-3'),
                    css_class='row',
                ),
                Div(
                    HTML('<span class="badge badge-default">11</span>'),
                    Div('student_address', css_class='col-md-3'),
                    HTML('<span class="badge badge-default">12</span>'),
                    Div('student_p_code', css_class='col-md-3'),
                    HTML('<span class="badge badge-default">13</span>'),
                    Div('disability', css_class='col-md-3'),
                    css_class='row',
                ),
                Div(
                    HTML('<span class="badge badge-default">14</span>'),
                    Div('outreach_barcode', css_class='col-md-3'),
                    css_class='row',
                ),
                css_class='bd-callout bd-callout-warning'
            ),
            Fieldset(
                None,
                Div(
                    HTML('<h4 id="alternatives-to-hidden-labels">Family Status</h4>')
                ),
                Div(
                    HTML('<span class="badge badge-default">1</span>'),
                    Div('hh_educational_level', css_class='col-md-3'),
                    HTML('<span class="badge badge-default">2</span>'),
                    Div('student_family_status', css_class='col-md-3'),
                    HTML('<span class="badge badge-default">3</span>'),
                    Div('student_have_children', css_class='col-md-3', css_id='student_have_children'),
                    css_class='row',
                ),
                Div(
                    HTML('<span class="badge badge-default">4</span>'),
                    Div('have_labour', css_class='col-md-3'),
                    HTML('<span class="badge badge-default">5</span>'),
                    Div('labours', css_class='col-md-3', css_id='labours'),
                    HTML('<span class="badge badge-default">6</span>'),
                    Div('labour_hours', css_class='col-md-3', css_id='labour_hours'),
                    css_class='row',
                ),
                css_class='bd-callout bd-callout-warning'
            ),
            Fieldset(
                None,
                Div(
                    HTML('<h4 id="alternatives-to-hidden-labels">Assessment</h4>')
                ),
                Div(
                    HTML('<div class="col-md-3"><a class="btn btn-success" href="'+pre_test+'">Pre-test</a></div>'),
                    HTML('<div class="col-md-3"><a class="btn btn-success" href="'+post_test+'">Post-test</a></div>'),
                    css_class='row',
                ),
                Div(
                    HTML('<div class="p-3"></div>'),
                    css_class='row'
                ),
                css_class='bd-callout bd-callout-warning'+display_assessment
            ),
            Fieldset(
                None,
                Div(
                    HTML('<h4 id="alternatives-to-hidden-labels">School Readiness</h4>')
                ),
                Div(
                    HTML('<span class="badge badge-default">1</span>'),
                    Div('participation', css_class='col-md-3'),
                    HTML('<span class="badge badge-default">2</span>'),
                    Div('barriers', css_class='col-md-3'),
                    HTML('<span class="badge badge-default">3</span>'),
                    Div('learning_result', css_class='col-md-3'),
                    css_class='row',
                ),
                css_class='bd-callout bd-callout-warning'+display_assessment
            ),
            FormActions(
                Submit('save', _('Save')),
                Button('cancel', _('Cancel')),
                HTML('<a class="btn btn-info" href="/youth/bln-list/">Back to list</a>'),
            )
        )

    def save(self, request=None, instance=None, serializer=None):
        super(BLNForm, self).save(request=request, instance=instance, serializer=BLNSerializer)

    class Meta:
        model = BLN
        fields = CommonForm.Meta.fields + (
            'cycle',
            'referral',
        )

    class Media:
        js = (
            'js/jquery-1.12.3.min.js',
            'js/jquery-ui-1.12.1.js',
            'js/validator.js',
            'js/registrations.js',
        )


class RSForm(CommonForm):

    cycle = forms.ModelChoiceField(
        queryset=RSCycle.objects.all(), widget=forms.Select,
        empty_label=_('Programme Cycle'),
        required=True, to_field_name='id',
        initial=0
    )

    site = forms.ModelChoiceField(
        queryset=Site.objects.all(), widget=forms.Select,
        empty_label=_('Programme Site'),
        required=False, to_field_name='id',
        initial=0
    )
    school = forms.ModelChoiceField(
        queryset=School.objects.all(), widget=forms.Select,
        empty_label=_('School'),
        required=False, to_field_name='id',
        initial=0
    )
    shift = forms.ChoiceField(
        widget=forms.Select, required=False,
        choices=RS.SCHOOL_SHIFT
    )

    def save(self, request=None, instance=None, serializer=None):
        super(RSForm, self).save()

    class Meta:
        model = RS
        fields = CommonForm.Meta.fields + (
            'cycle',
            'site',
            'school',
            'shift',
        )


class CBECEForm(CommonForm):

    cycle = forms.ModelChoiceField(
        queryset=Cycle.objects.all(), widget=forms.Select,
        empty_label=_('Programme Cycle'),
        required=False, to_field_name='id',
        initial=0
    )
    site = forms.ModelChoiceField(
        queryset=Site.objects.all(), widget=forms.Select,
        empty_label=_('Programme Site'),
        required=False, to_field_name='id',
        initial=0
    )
    school = forms.ModelChoiceField(
        queryset=School.objects.all(), widget=forms.Select,
        empty_label=_('School'),
        required=False, to_field_name='id',
        initial=0
    )
    referral = forms.MultipleChoiceField(
        choices=CLM.REFERRAL,
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )
    child_muac = forms.ChoiceField(
        widget=forms.Select, required=True,
        choices=CBECE.MUAC
    )

    def save(self, request=None, instance=None, serializer=None):
        super(CBECEForm, self).save()

    class Meta:
        model = CBECE
        fields = CommonForm.Meta.fields + (
            'cycle',
            'site',
            'school',
            'referral',
            'child_muac',
        )
