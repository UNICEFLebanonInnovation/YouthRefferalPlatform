# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import json
import tablib


from django.views.generic import ListView, FormView, TemplateView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import RedirectView
from django.utils.translation import ugettext as _

from rest_framework import status
from rest_framework import viewsets, mixins, permissions

from rest_framework.generics import DestroyAPIView
from django_filters.views import FilterView
from django_tables2 import RequestConfig, SingleTableView
from django_tables2.export.views import ExportMixin

from import_export.formats import base_formats

from referral_platform.users.views import UserRegisteredMixin
from referral_platform.users.utils import force_default_language
from referral_platform.youth.models import YoungPerson
from .serializers import RegistrationSerializer
from .models import Registration, Assessment, AssessmentSubmission
from .filters import YouthFilter, YouthPLFilter, YouthSYFilter
from .tables import BootstrapTable, CommonTable
from .forms import CommonForm


class ListingView(LoginRequiredMixin,
                  FilterView,
                  ExportMixin,
                  SingleTableView,
                  RequestConfig):

    table_class = CommonTable
    model = Registration
    template_name = 'registration/list.html'
    table = BootstrapTable(Registration.objects.all(), order_by='id')

    filterset_class = YouthFilter

    def get_queryset(self):
        return Registration.objects.filter(partner_organization=self.request.user.partner)

    def get_filterset_class(self):
        locations = [g.p_code for g in self.request.user.partner.locations.all()]
        if "PALESTINE" in locations:
            print("in like flynn")
            return YouthPLFilter
        elif "SYRIA" in locations:
            return YouthSYFilter
        elif "JORDAN" in locations:
            return YouthFilter


class AddView(LoginRequiredMixin, CreateView):
    template_name = 'registration/form.html'
    form_class = CommonForm
    model = Registration
    success_url = '/registration/list/'

    def get_success_url(self):
        if self.request.POST.get('save_add_another', None):
            return '/registration/add/'
        return self.success_url

    def get_initial(self):
        data = dict()
        if self.request.user.partner:
            data['partner_locations'] = self.request.user.partner.locations.all()
            data['partner'] = self.request.user.partner
        initial = data
        return initial

    def form_valid(self, form):
        form.save(self.request)
        return super(AddView, self).form_valid(form)


class EditView(LoginRequiredMixin, UpdateView):
    template_name = 'registration/form.html'
    form_class = CommonForm
    model = Registration
    success_url = '/registration/list/'

    def get_success_url(self):
        if self.request.POST.get('save_add_another', None):
            return '/registration/add/'
        return self.success_url

    def get_initial(self):
        data = dict()
        if self.request.user.partner:
            data['partner_locations'] = self.request.user.partner.locations.all()
            data['partner'] = self.request.user.partner
        initial = data
        return initial

    def get_form(self, form_class=None):
        instance = Enrollment.objects.get(id=self.kwargs['pk'])
        if self.request.method == "POST":
            return CommonForm(self.request.POST, instance=instance)
        else:
            data = RegistrationSerializer(instance).data
            data['student_nationality'] = data['student_nationality_id']
            return CommonForm(data, instance=instance)

    def form_valid(self, form):
        instance = Registration.objects.get(id=self.kwargs['pk'])
        form.save(request=self.request, instance=instance)
        return super(EditView, self).form_valid(form)


class YouthAssessment(SingleObjectMixin, RedirectView):
    model = Assessment

    def get_redirect_url(self, *args, **kwargs):
        assessment = self.get_object()
        registry = Registration.objects.get(id=self.request.GET.get('registration'))
        youth = registry.youth

        url = '{form}?d[country]={country}&d[governorate]={governorate}&d[partner]={partner}&d[center]={center}&d[' \
              'first]={first}&d[last]={last}&d[father]={father}&d[nationality]={nationality}&d[gender]={gender}&d[' \
              'birthdate]={birthdate}&d[youth_id]={youth_id}&d[registry]={registry}&d[marital]={marital}&d[bayanati]={bayanati_id}&d[slug]={' \
              'slug}&d[status]=enrolled&returnURL={callback}'.format(
            form=assessment.assessment_form,
            slug=assessment.slug,
            country=youth.governorate.parent.name,
            governorate=youth.governorate.name,
            partner=youth.partner_organization.name,
            center=youth.center.name if youth.center else "",
            first=youth.first_name,
            father=youth.father_name,
            last=youth.last_name,
            nationality=youth.nationality.name,
            gender=youth.sex,
            marital=youth.marital_status,
            birthdate=youth.birthday_year + "-" + '{0:0>2}'.format(len(youth.birthday_month)) + "-" + '{0:0>2}'.format(
                len(youth.birthday_day)),
            youth_id=youth.number,
            registry=registry.id,
            bayanati_id=youth.bayanati_ID if youth.bayanati_ID else "",
            status=self.request.GET.get('status'),
            callback=self.request.META.get('HTTP_REFERER', youth.get_absolute_url())
        )
        return url


@method_decorator(csrf_exempt, name='dispatch')
class YouthAssessmentSubmission(SingleObjectMixin, View):
    def post(self, request, *args, **kwargs):
        if 'youth_id' not in request.body or 'status' not in request.body:
            return HttpResponseBadRequest()

        payload = json.loads(request.body.decode('utf-8'))

        registration = Registration.objects.get(id=payload['registry'])
        assessment = Assessment.objects.get(slug=payload['slug'])
        submission, new = AssessmentSubmission.objects.get_or_create(
            registration=registration,
            youth=registration.youth,
            assessment=assessment,
            status=payload['status']
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
        return self.queryset.filter(partner_organization=self.request.user.partner)

    def delete(self, request, *args, **kwargs):
        instance = self.model.objects.get(id=kwargs['pk'])
        instance.delete()
        return JsonResponse({'status': status.HTTP_200_OK})


class ExportView(LoginRequiredMixin, ListView):

    model = YoungPerson
    queryset = YoungPerson.objects.all()

    def get(self, request, *args, **kwargs):

        book = tablib.Databook()
        data = tablib.Dataset()
        data.title = "TEST"
        data.headers = [
            _('Governorate'),
            _('Trainer'),
            _('Location'),
            _('Bayanati ID'),
            _('First name'),
            _('Father name'),
            _('Last name'),
            _('Sex'),
            _('birthday day'),
            _('birthday month'),
            _('birthday year'),
            _('age'),
            _('Birthday'),
            _('Nationality'),
            _('Marital status'),
            _('address'),
        ]

        queryset = self.queryset.filter(youth__partner_organization=self.request.user.partner)

        content = []
        for line in queryset:
            content = [
                line.governorate.name,
                line.trainer,
                line.location,
                line.bayanati_ID,
                line.first_name,
                line.father_name,
                line.last_name,
                line.sex,
                line.birthday_day,
                line.birthday_month,
                line.birthday_year,
                line.calc_age,
                line.birthday,
                line.nationality.name,
                line.marital_status,
                line.address,
            ]
            data.append(content)
        book.add_sheet(data)

        response = HttpResponse(
            book.export("xls"),
            content_type='application/vnd.ms-excel',
        )
        response['Content-Disposition'] = 'attachment; filename=youth_list.xls'
        return response
