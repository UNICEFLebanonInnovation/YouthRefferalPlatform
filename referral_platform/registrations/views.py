# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import json
import tablib
import datetime
import time

from django.views.generic import ListView, FormView, TemplateView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import RedirectView
from django.utils.translation import ugettext as _

from rest_framework import status
from rest_framework import viewsets, mixins, permissions

from django_filters.views import FilterView
from django_tables2 import RequestConfig, SingleTableView
from django_tables2.export.views import ExportMixin

from referral_platform.youth.models import YoungPerson
from .serializers import RegistrationSerializer, AssessmentSubmissionSerializer
from .models import Registration, Assessment, AssessmentSubmission, AssessmentHash
from .filters import YouthFilter, YouthPLFilter, YouthSYFilter
from .tables import BootstrapTable, CommonTable, CommonTableAlt
from .forms import CommonForm


class ListingView(LoginRequiredMixin,
                  FilterView,
                  ExportMixin,
                  SingleTableView,
                  RequestConfig):

    table_class = CommonTable
    model = Registration
    template_name = 'registrations/list.html'
    table = BootstrapTable(Registration.objects.all(), order_by='id')

    filterset_class = YouthFilter

    def get_queryset(self):
        return Registration.objects.filter(partner_organization=self.request.user.partner)

    def get_filterset_class(self):
        locations = [g.p_code for g in self.request.user.partner.locations.all()]
        if "PALESTINE" in locations:
            return YouthPLFilter
        elif "SYRIA" in locations:
            return YouthSYFilter
        elif "JORDAN" in locations:
            return YouthFilter

    def get_table_class(self):
            locations = [g.p_code for g in self.request.user.partner.locations.all()]
            if "PALESTINE" in locations:
                return CommonTableAlt
            elif "SYRIA" in locations:
                return CommonTableAlt
            elif "JORDAN" in locations:
                return CommonTable


class AddView(LoginRequiredMixin, FormView):

    template_name = 'registrations/form.html'
    form_class = CommonForm
    model = Registration
    success_url = '/registrations/list/'

    def get_success_url(self):
        if self.request.POST.get('save_add_another', None):
            return '/registrations/add/'
        return self.success_url

    def get_initial(self):
        data = dict()
        if self.request.user.partner:
            data['partner_locations'] = self.request.user.partner.locations.all()
            data['partner'] = self.request.user.partner

        if self.request.GET.get('youth_id'):
                instance = YoungPerson.objects.get(id=self.request.GET.get('youth_id'))
                data['youth_id'] = instance.id
                data['youth_first_name'] = instance.first_name
                data['youth_father_name'] = instance.father_name
                data['youth_last_name'] = instance.last_name
                data['youth_birthday_day'] = instance.birthday_day
                data['youth_birthday_month'] = instance.birthday_month
                data['youth_birthday_year'] = instance.birthday_year
                data['youth_sex'] = instance.sex
                data['youth_nationality'] = instance.nationality_id
                data['youth_marital_status'] = instance.marital_status

        initial = data
        return initial

    def form_valid(self, form):
        form.save(request=self.request)
        return super(AddView, self).form_valid(form)


class EditView(LoginRequiredMixin, FormView):
    template_name = 'registrations/form.html'
    form_class = CommonForm
    model = Registration
    success_url = '/registrations/list/'

    def get_success_url(self):
        if self.request.POST.get('save_add_another', None):
            return '/registrations/add/'
        return self.success_url

    def get_initial(self):
        data = dict()
        if self.request.user.partner:
            data['partner_locations'] = self.request.user.partner.locations.all()
            data['partner'] = self.request.user.partner
        initial = data
        return initial

    def get_form(self, form_class=None):
        instance = Registration.objects.get(id=self.kwargs['pk'], partner_organization=self.request.user.partner)
        if self.request.method == "POST":
            return CommonForm(self.request.POST, instance=instance)
        else:
            data = RegistrationSerializer(instance).data
            data['youth_nationality'] = data['youth_nationality_id']
            data['partner_locations'] = self.request.user.partner.locations.all()
            data['partner'] = self.request.user.partner
            return CommonForm(data, instance=instance)

    def form_valid(self, form):
        instance = Registration.objects.get(id=self.kwargs['pk'], partner_organization=self.request.user.partner)
        form.save(request=self.request, instance=instance)
        return super(EditView, self).form_valid(form)


class YouthAssessment(SingleObjectMixin, RedirectView):
    model = Assessment

    def get_redirect_url(self, *args, **kwargs):
        assessment = self.get_object()
        registry = Registration.objects.get(id=self.request.GET.get('registry'),
                                            partner_organization=self.request.user.partner)
        youth = registry.youth
        hashing = AssessmentHash.objects.create(
            registration=registry.id,
            assessment_slug=assessment.slug,
            partner=self.request.user.partner_id,
            user=self.request.user.id,
            timestamp=time.time()
        )

        url = '{form}?d[registry]={registry}&d[country]={country}&d[nationality]={nationality}' \
              '&returnURL={callback}'.format(
                form=assessment.assessment_form,
                registry=hashing.hashed,
                country=registry.governorate.parent.name,
                nationality=youth.nationality.code,
                callback=self.request.META.get('HTTP_REFERER', registry.get_absolute_url())
        )
        return url


@method_decorator(csrf_exempt, name='dispatch')
class YouthAssessmentSubmission(SingleObjectMixin, View):
    def post(self, request, *args, **kwargs):
        if 'registry' not in request.body:
            return HttpResponseBadRequest()

        payload = json.loads(request.body.decode('utf-8'))

        hashing = AssessmentHash.objects.get(hashed=payload['registry'])

        registration = Registration.objects.get(id=int(hashing.registration))
        assessment = Assessment.objects.get(slug=hashing.assessment_slug)
        submission, new = AssessmentSubmission.objects.get_or_create(
            registration=registration,
            youth=registration.youth,
            assessment=assessment,
            status='enrolled'
        )
        submission.data = payload
        submission.save()

        return HttpResponse()


class RegistrationViewSet(mixins.RetrieveModelMixin,
                          mixins.ListModelMixin,
                          mixins.CreateModelMixin,
                          mixins.UpdateModelMixin,
                          viewsets.GenericViewSet):

    model = Registration
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        if self.request.method in ["PATCH", "POST", "PUT"]:
            return self.queryset
        return self.queryset.filter(partner_organization=self.request.user.partner)

    def delete(self, request, *args, **kwargs):
        instance = self.model.objects.get(id=kwargs['pk'], partner_organization=self.request.user.partner)
        instance.delete()
        return JsonResponse({'status': status.HTTP_200_OK})


class AssessmentSubmissionViewSet(mixins.CreateModelMixin,
                                  mixins.UpdateModelMixin,
                                  viewsets.GenericViewSet):

    model = AssessmentSubmission
    queryset = AssessmentSubmission.objects.all()
    serializer_class = AssessmentSubmissionSerializer
    permission_classes = (permissions.IsAuthenticated,)


class ExportView(LoginRequiredMixin, ListView):

    model = Registration
    queryset = Registration.objects.all()

    def get(self, request, *args, **kwargs):

        if self.request.user.is_superuser and not self.request.user.partner:
            queryset = self.queryset
        else:
            queryset = self.queryset.filter(partner_organization=self.request.user.partner)

        gov = self.request.GET.get('governorate', 0)
        if gov:
            queryset = queryset.filter(governorate_id=int(gov))

        common_headers = [
            _('Country'),
            _('Governorate'),
            _('Location'),
            _('Partner'),

            _('Unique number'),
            _('First name'),
            _('Father name'),
            _('Last name'),
            _('Trainer'),
            _('Bayanati ID'),
            _('Sex'),
            _('birthday day'),
            _('birthday month'),
            _('birthday year'),
            _('age'),
            _('Birthday'),
            _('Nationality'),
            _('Marital status'),
            _('address'),
            _('Submission date'),
        ]

        book = tablib.Databook()
        data = tablib.Dataset()
        data.title = "Beneficiary List"
        data.headers = common_headers

        content = []
        for line in queryset:
            youth = line.youth
            content = [
                line.governorate.parent.name if line.governorate else '',
                line.governorate.name if line.governorate else '',
                line.location,
                line.partner_organization.name if line.partner_organization else '',

                youth.number,
                youth.first_name,
                youth.father_name,
                youth.last_name,
                line.trainer,
                youth.bayanati_ID,
                youth.sex,
                youth.birthday_day,
                youth.birthday_month,
                youth.birthday_year,
                youth.calc_age,
                youth.birthday,
                youth.nationality.name,
                youth.marital_status,
                youth.address,
                line.created.strftime('%d/%m/%Y') if line.created else '',
            ]
            data.append(content)

        book.add_sheet(data)

        response = HttpResponse(
            book.export("xls"),
            content_type='application/vnd.ms-excel',
        )
        response['Content-Disposition'] = 'attachment; filename=Beneficiary_list.xls'
        return response


class ExportRegistryAssessmentsView(LoginRequiredMixin, ListView):

    model = AssessmentSubmission
    queryset = AssessmentSubmission.objects.filter(assessment__slug='registration')

    def get(self, request, *args, **kwargs):

        book = tablib.Databook()

        if self.request.user.is_superuser and not self.request.user.partner:
            submission_set = self.queryset
        else:
            submission_set = self.queryset.filter(registration__partner_organization=self.request.user.partner)

        gov = self.request.GET.get('governorate', 0)
        if gov:
            submission_set = submission_set.filter(registration__governorate_id=int(gov))

        data2 = tablib.Dataset()
        data2.title = "Registration Assessment"
        data2.headers = [
            _('Country'),
            _('Governorate'),
            _('Location'),
            _('Partner'),

            _('Unique number'),
            _('First name'),
            _('Father name'),
            _('Last name'),
            _('Trainer'),
            _('Bayanati ID'),
            _('Sex'),
            _('birthday day'),
            _('birthday month'),
            _('birthday year'),
            _('age'),
            _('Birthday'),
            _('Nationality'),
            _('Marital status'),
            _('address'),

            _('training_type'),
            _('center_type'),
            _('concent_paper'),
            _('If_you_answered_Othe_the_name_of_the_NGO'),
            _('UNHCR_ID'),
            _('Jordanian_ID'),
            _('training_date'),
            _('training_end_date'),
            _('educational_status'),
            _('school_level'),
            _('School_type'),
            _('School_name'),
            _('how_many_times_skipped_school'),
            _('reason_for_skipping_class'),
            _('educ_level_stopped'),
            _('Reason_stop_study'),
            _('other_five'),
            _('Relation_with_labor_market'),
            _('occupation_type'),
            _('what_electronics_do_you_own'),
            _('family_present'),
            _('family_not_present'),
            _('not_present_where'),
            _('other_family_not_present'),
            _('drugs_substance_use'),
            _('feeling_of_safety_security'),
            _('reasons_for_not_feeling_safe_a'),
            _('Accommodation_type'),
            _('how_many_times_displaced'),
            _('family_steady_income'),
            _('desired_method_for_follow_up'),
            _('text_39911992'),
            _('text_d45750c6'),
            _('text_4c6fe6c9'),
            _('submission_time'),
        ]

        for line2 in submission_set:
            content = []
            youth = line2.youth
            registry = line2.registration
            submission_date = line2.data.get('_submission_time', '')
            try:
                submission_date = datetime.datetime.strptime(submission_date, '%Y-%m-%dT%H:%M:%S').strftime(
                    '%d/%m/%Y') if submission_date else ''
            except Exception:
                submission_date = ''
            content = [
                registry.governorate.parent.name if registry.governorate else '',
                registry.governorate.name if registry.governorate else '',
                registry.location,
                registry.partner_organization.name if registry.partner_organization else '',

                youth.number,
                youth.first_name,
                youth.father_name,
                youth.last_name,
                registry.trainer,
                youth.bayanati_ID,
                youth.sex,
                youth.birthday_day,
                youth.birthday_month,
                youth.birthday_year,
                youth.calc_age,
                youth.birthday,
                youth.nationality.name if youth.nationality else '',
                youth.marital_status,
                youth.address,

                line2.data.get('training_type', ''),
                line2.data.get('center_type', ''),
                line2.data.get('concent_paper', ''),
                line2.data.get('If_you_answered_Othe_the_name_of_the_NGO', ''),
                line2.data.get('UNHCR_ID', ''),
                line2.data.get('Jordanian_ID', ''),
                line2.data.get('training_date', ''),
                line2.data.get('training_end_date', ''),
                line2.data.get('educational_status', ''),
                line2.data.get('school_level', ''),
                line2.data.get('School_type', ''),
                line2.data.get('School_name', ''),
                line2.data.get('how_many_times_skipped_school', ''),
                line2.data.get('reason_for_skipping_class', ''),
                line2.data.get('educ_level_stopped', ''),
                line2.data.get('Reason_stop_study', ''),
                line2.data.get('other_five', ''),
                line2.data.get('Relation_with_labor_market', ''),
                line2.data.get('occupation_type', ''),
                line2.data.get('what_electronics_do_you_own', ''),
                line2.data.get('family_present', ''),
                line2.data.get('family_not_present', ''),
                line2.data.get('not_present_where', ''),
                line2.data.get('other_family_not_present', ''),
                line2.data.get('drugs_substance_use', ''),
                line2.data.get('feeling_of_safety_security', ''),
                line2.data.get('reasons_for_not_feeling_safe_a', ''),
                line2.data.get('Accommodation_type', ''),
                line2.data.get('how_many_times_displaced', ''),
                line2.data.get('family_steady_income', ''),
                line2.data.get('desired_method_for_follow_up', ''),
                line2.data.get('text_39911992', ''),
                line2.data.get('text_d45750c6', ''),
                line2.data.get('text_4c6fe6c9', ''),
                submission_date,
            ]
            data2.append(content)

        book.add_sheet(data2)

        response = HttpResponse(
            book.export("xls"),
            content_type='application/vnd.ms-excel',
        )
        response['Content-Disposition'] = 'attachment; filename=Beneficiary_Registration_Assessments.xls'
        return response


class ExportCivicAssessmentsView(LoginRequiredMixin, ListView):

    model = AssessmentSubmission
    queryset = AssessmentSubmission.objects.all()

    def get(self, request, *args, **kwargs):

        book = tablib.Databook()

        if self.request.user.is_superuser and not self.request.user.partner:
            submission_set = self.queryset
        else:
            submission_set = self.queryset.filter(registration__partner_organization=self.request.user.partner)

        gov = self.request.GET.get('governorate', 0)
        if gov:
            submission_set = submission_set.filter(registration__governorate_id=int(gov))

        data3 = tablib.Dataset()
        data3.title = "Pre-Assessment"
        data3.headers = [
            _('Country'),
            _('Governorate'),
            _('Location'),
            _('Partner'),

            _('Unique number'),
            _('First name'),
            _('Father name'),
            _('Last name'),
            _('Trainer'),
            _('Bayanati ID'),
            _('Sex'),
            _('birthday day'),
            _('birthday month'),
            _('birthday year'),
            _('age'),
            _('Birthday'),
            _('Nationality'),
            _('Marital status'),
            _('address'),

            _('_4_articulate_thoughts'),
            _('_1_express_opinion'),
            _('discuss_before_decision'),
            _('_28_discuss_opinions'),
            _('_31_willing_to_compromise'),
            _('_pal_I_belong'),
            _('_41_where_to_volunteer'),
            _('_42_regularly_volunteer'),
            _('_pal_contrib_appreciated'),
            _('_pal_contribute_to_development'),
            _('_51_communicate_community_conc'),
            _('_52_participate_community_medi'),
            _('submission time'),
        ]

        data4 = tablib.Dataset()
        data4.title = "Post-Assessment"
        data4.headers = [
            _('Country'),
            _('Governorate'),
            _('Location'),
            _('Partner'),

            _('Unique number'),
            _('First name'),
            _('Father name'),
            _('Last name'),
            _('Trainer'),
            _('Bayanati ID'),
            _('Sex'),
            _('birthday day'),
            _('birthday month'),
            _('birthday year'),
            _('age'),
            _('Birthday'),
            _('Nationality'),
            _('Marital status'),
            _('address'),

            _('_4_articulate_thoughts'),
            _('_1_express_opinion'),
            _('_20_discussions_with_peers_before_'),
            _('_28_discuss_opinions'),
            _('_31_willing_to_compromise'),
            _('_pal_I_belong'),
            _('_41_where_to_volunteer'),
            _('_42_regularly_volunteer'),
            _('_pal_contrib_appreciated'),
            _('_pal_contribute_to_development'),
            _('_51_communicate_community_conc'),
            _('_52_participate_community_medi'),
            _('submission time')
        ]

        submission_set1 = submission_set.filter(assessment__slug='pre_assessment')
        for line2 in submission_set1:
            youth = line2.youth
            registry = line2.registration
            submission_date = line2.data.get('_submission_time', '')
            try:
                submission_date = datetime.datetime.strptime(submission_date, '%Y-%m-%dT%H:%M:%S').strftime(
                    '%d/%m/%Y') if submission_date else ''
            except Exception:
                submission_date = ''
            content = [
                registry.governorate.parent.name if registry.governorate else '',
                registry.governorate.name if registry.governorate else '',
                registry.location,
                registry.partner_organization.name if registry.partner_organization else '',

                youth.number,
                youth.first_name,
                youth.father_name,
                youth.last_name,
                registry.trainer,
                youth.bayanati_ID,
                youth.sex,
                youth.birthday_day,
                youth.birthday_month,
                youth.birthday_year,
                youth.calc_age,
                youth.birthday,
                youth.nationality.name if youth.nationality else '',
                youth.marital_status,
                youth.address,

                line2.data.get('_4_articulate_thoughts', ''),
                line2.data.get('_1_express_opinion', ''),
                line2.data.get('discuss_before_decision', ''),
                line2.data.get('_28_discuss_opinions', ''),
                line2.data.get('_31_willing_to_compromise', ''),
                line2.data.get('_pal_I_belong', ''),
                line2.data.get('_41_where_to_volunteer', ''),
                line2.data.get('_42_regularly_volunteer', ''),
                line2.data.get('_pal_contrib_appreciated', ''),
                line2.data.get('_pal_contribute_to_development', ''),
                line2.data.get('_51_communicate_community_conc', ''),
                line2.data.get('_52_participate_community_medi', ''),
                submission_date,
            ]
            data3.append(content)

        submission_set2 = submission_set.filter(assessment__slug='post_assessment')
        for line2 in submission_set2:
            youth = line2.youth
            registry = line2.registration
            submission_date = line2.data.get('_submission_time', '')
            try:
                submission_date = datetime.datetime.strptime(submission_date, '%Y-%m-%dT%H:%M:%S').strftime(
                    '%d/%m/%Y') if submission_date else ''
            except Exception:
                submission_date = ''
            content = [
                registry.governorate.parent.name if registry.governorate else '',
                registry.governorate.name if registry.governorate else '',
                registry.location,
                registry.partner_organization.name if registry.partner_organization else '',

                youth.number,
                youth.first_name,
                youth.father_name,
                youth.last_name,
                registry.trainer,
                youth.bayanati_ID,
                youth.sex,
                youth.birthday_day,
                youth.birthday_month,
                youth.birthday_year,
                youth.calc_age,
                youth.birthday,
                youth.nationality.name if youth.nationality else '',
                youth.marital_status,
                youth.address,

                line2.data.get('_4_articulate_thoughts', ''),
                line2.data.get('_1_express_opinion', ''),
                line2.data.get('_20_discussions_with_peers_before_', ''),
                line2.data.get('_28_discuss_opinions', ''),
                line2.data.get('_31_willing_to_compromise', ''),
                line2.data.get('_pal_I_belong', ''),
                line2.data.get('_41_where_to_volunteer', ''),
                line2.data.get('_42_regularly_volunteer', ''),
                line2.data.get('_pal_contrib_appreciated', ''),
                line2.data.get('_pal_contribute_to_development', ''),
                line2.data.get('_51_communicate_community_conc', ''),
                line2.data.get('_52_participate_community_medi', ''),
                submission_date,
            ]
            data4.append(content)

        book.add_sheet(data3)
        book.add_sheet(data4)

        response = HttpResponse(
            book.export("xls"),
            content_type='application/vnd.ms-excel',
        )
        response['Content-Disposition'] = 'attachment; filename=Beneficiary_Civic_Engagement_Assessments.xls'
        return response


class ExportEntrepreneurshipAssessmentsView(LoginRequiredMixin, ListView):

    model = AssessmentSubmission
    queryset = AssessmentSubmission.objects.all()

    def get(self, request, *args, **kwargs):

        book = tablib.Databook()

        if self.request.user.is_superuser and not self.request.user.partner:
            submission_set = self.queryset
        else:
            submission_set = self.queryset.filter(registration__partner_organization=self.request.user.partner)

        gov = self.request.GET.get('governorate', 0)
        if gov:
            submission_set = submission_set.filter(registration__governorate_id=int(gov))

        data5 = tablib.Dataset()
        data5.title = "Pre-Entrepreneurship"
        data5.headers = [
            _('Country'),
            _('Governorate'),
            _('Location'),
            _('Partner'),

            _('Unique number'),
            _('First name'),
            _('Father name'),
            _('Last name'),
            _('Trainer'),
            _('Bayanati ID'),
            _('Sex'),
            _('birthday day'),
            _('birthday month'),
            _('birthday year'),
            _('age'),
            _('Birthday'),
            _('Nationality'),
            _('Marital status'),
            _('address'),

            _('can_plan_personal'),
            _('can_plan_career'),
            _('can_manage_financ'),
            _('can_plan_time'),
            _('can_suggest'),
            _('can_take_decision'),
            _('can_determin_probs'),
            _('aware_resources'),
            _('can_handle_pressure'),
            _('motivated_advance_skills'),
            _('communication_skills'),
            _('presentation_skills'),
            _('team_is'),
            _('good_team_is'),
            _('team_leader_is'),
            _('bad_decision_cause'),
            _('easiest_solution'),
            _('problem_solving'),
            _('submission time'),
        ]

        data6 = tablib.Dataset()
        data6.title = "Post-Entrepreneurship"
        data6.headers = [
            _('Country'),
            _('Governorate'),
            _('Location'),
            _('Partner'),

            _('Unique number'),
            _('First name'),
            _('Father name'),
            _('Last name'),
            _('Trainer'),
            _('Bayanati ID'),
            _('Sex'),
            _('birthday day'),
            _('birthday month'),
            _('birthday year'),
            _('age'),
            _('Birthday'),
            _('Nationality'),
            _('Marital status'),
            _('address'),

            _('can_plan_personal'),
            _('can_plan_career'),
            _('can_manage_financ'),
            _('can_plan_time'),
            _('can_suggest'),
            _('can_take_decision'),
            _('can_determin_probs'),
            _('aware_resources'),
            _('can_handle_pressure'),
            _('motivated_advance_skills'),
            _('communication_skills'),
            _('presentation_skills'),
            _('team_is'),
            _('good_team_is'),
            _('team_leader_is'),
            _('bad_decision_cause'),
            _('easiest_solution'),
            _('problem_solving'),
            _('personal_value'),
            _('faced_challenges'),
            _('challenges'),
            _('bad_venue'),
            _('bad_venue_others'),
            _('has_comments'),
            _('additional_comments'),
            _('submission_time'),
        ]

        submission_set1 = submission_set.filter(assessment__slug='pre_entrepreneurship')
        for line2 in submission_set1:
            youth = line2.youth
            registry = line2.registration
            submission_date = line2.data.get('_submission_time', '')
            try:
                submission_date = datetime.datetime.strptime(submission_date, '%Y-%m-%dT%H:%M:%S').strftime(
                    '%d/%m/%Y') if submission_date else ''
            except Exception:
                submission_date = ''

            content = [
                registry.governorate.parent.name if registry.governorate else '',
                registry.governorate.name if registry.governorate else '',
                registry.location,
                registry.partner_organization.name if registry.partner_organization else '',

                youth.number,
                youth.first_name,
                youth.father_name,
                youth.last_name,
                registry.trainer,
                youth.bayanati_ID,
                youth.sex,
                youth.birthday_day,
                youth.birthday_month,
                youth.birthday_year,
                youth.calc_age,
                youth.birthday,
                youth.nationality.name if youth.nationality else '',
                youth.marital_status,
                youth.address,

                line2.data.get('can_plan_personal', ''),
                line2.data.get('can_plan_career', ''),
                line2.data.get('can_manage_financ', ''),
                line2.data.get('can_plan_time', ''),
                line2.data.get('can_suggest', ''),
                line2.data.get('can_take_decision', ''),
                line2.data.get('can_determin_probs', ''),
                line2.data.get('aware_resources', ''),
                line2.data.get('can_handle_pressure', ''),
                line2.data.get('motivated_advance_skills', ''),
                line2.data.get('communication_skills', ''),
                line2.data.get('presentation_skills', ''),
                line2.data.get('team_is', ''),
                line2.data.get('good_team_is', ''),
                line2.data.get('team_leader_is', ''),
                line2.data.get('bad_decision_cause', ''),
                line2.data.get('easiest_solution', ''),
                line2.data.get('problem_solving', ''),
                submission_date,
            ]
            data5.append(content)

        submission_set2 = submission_set.filter(assessment__slug='post_entrepreneurship')
        for line2 in submission_set2:
            youth = line2.youth
            registry = line2.registration
            submission_date = line2.data.get('_submission_time', '')
            try:
                submission_date = datetime.datetime.strptime(submission_date, '%Y-%m-%dT%H:%M:%S').strftime(
                    '%d/%m/%Y') if submission_date else ''
            except Exception:
                submission_date = ''
            content = [
                registry.governorate.parent.name if registry.governorate else '',
                registry.governorate.name if registry.governorate else '',
                registry.location,
                registry.partner_organization.name if registry.partner_organization else '',

                youth.number,
                youth.first_name,
                youth.father_name,
                youth.last_name,
                registry.trainer,
                youth.bayanati_ID,
                youth.sex,
                youth.birthday_day,
                youth.birthday_month,
                youth.birthday_year,
                youth.calc_age,
                youth.birthday,
                youth.nationality.name if youth.nationality else '',
                youth.marital_status,
                youth.address,

                line2.data.get('can_plan_personal', ''),
                line2.data.get('can_plan_career', ''),
                line2.data.get('can_manage_financ', ''),
                line2.data.get('can_plan_time', ''),
                line2.data.get('can_suggest', ''),
                line2.data.get('can_take_decision', ''),
                line2.data.get('can_determin_probs', ''),
                line2.data.get('aware_resources', ''),
                line2.data.get('can_handle_pressure', ''),
                line2.data.get('motivated_advance_skills', ''),
                line2.data.get('communication_skills', ''),
                line2.data.get('presentation_skills', ''),
                line2.data.get('team_is', ''),
                line2.data.get('good_team_is', ''),
                line2.data.get('team_leader_is', ''),
                line2.data.get('bad_decision_cause', ''),
                line2.data.get('easiest_solution', ''),
                line2.data.get('problem_solving', ''),
                line2.data.get('personal_value', ''),
                line2.data.get('faced_challenges', ''),
                line2.data.get('challenges', ''),
                line2.data.get('bad_venue', ''),
                line2.data.get('bad_venue_others', ''),
                line2.data.get('has_comments', ''),
                line2.data.get('additional_comments', ''),
                submission_date,
            ]
            data6.append(content)

        book.add_sheet(data5)
        book.add_sheet(data6)

        response = HttpResponse(
            book.export("xls"),
            content_type='application/vnd.ms-excel',
        )
        response['Content-Disposition'] = 'attachment; filename=Beneficiary_Entrepreneurship_Assessments.xls'
        return response
