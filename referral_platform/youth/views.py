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
from referral_platform.clm.models import Assessment, AssessmentSubmission
from .models import YoungPerson
from .filters import YouthFilter
from .tables import BootstrapTable, CommonTable
from .forms import CommonForm, RegistrationForm


class ListingView(LoginRequiredMixin,
                  FilterView,
                  ExportMixin,
                  SingleTableView,
                  RequestConfig):

    table_class = CommonTable
    model = YoungPerson
    template_name = 'youth/list.html'
    table = BootstrapTable(YoungPerson.objects.all(), order_by='id')

    filterset_class = YouthFilter

    def get_queryset(self):
        return YoungPerson.objects.filter(partner_organization=self.request.user.partner)


class AddView(LoginRequiredMixin, CreateView):
    template_name = 'youth/form.html'
    form_class = CommonForm
    model = YoungPerson
    success_url = '/youth/'

    def get_success_url(self):
        if self.request.POST.get('save_add_another', None):
            return '/youth/add/'
        return self.success_url

    def get_initial(self):
        data = dict()
        if self.request.user.partner:
            data['partner_locations'] = self.request.user.partner.locations.all()
            data['partner'] = self.request.user.partner
        initial = data
        return initial

    def form_valid(self, form):
        instance = form.save(self.request)
        instance.partner_organization = self.request.user.partner
        instance.save()

        return super(AddView, self).form_valid(form)


class DeleteYouthView(mixins.RetrieveModelMixin,
                 mixins.ListModelMixin,
                 mixins.CreateModelMixin,
                 mixins.UpdateModelMixin,
                 #viewsets.GenericViewSet,
                 DestroyAPIView):
    """
    Provides API operations around a Enrollment record
    TAREK NOTES: REVERT THIS TO USE API MODULE to USE FULL CRUD OPERATIONS.
    """
    queryset = YoungPerson.objects.all()

    @csrf_exempt
    def delete(self, request, *args, **kwargs):
        return super(DeleteYouthView, self).delete(request, *args, **kwargs)


class EditView(LoginRequiredMixin, UpdateView):
    template_name = 'youth/form.html'
    form_class = CommonForm
    model = YoungPerson
    success_url = '/youth/'

    def get_success_url(self):
        if self.request.POST.get('save_add_another', None):
            return '/youth/add/'
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
        return super(EditView, self).form_valid(form)


class YouthAssessment(SingleObjectMixin, RedirectView):
    model = Assessment

    def get_redirect_url(self, *args, **kwargs):
        assessment = self.get_object()
        youth = YoungPerson.objects.get(number=self.request.GET.get('youth_id'))

        url = '{form}?d[country]={country}&d[governorate]={governorate}&d[partner]={partner}&d[center]={center}&d[' \
              'first]={first}&d[last]={last}&d[father]={father}&d[nationality]={nationality}&d[gender]={gender}&d[' \
              'birthdate]={birthdate}&d[youth_id]={youth_id}&d[marital]={marital}&d[bayanati]={bayanati_id}&d[slug]={' \
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

        youth = YoungPerson.objects.get(number=payload['youth_id'])
        assessment = Assessment.objects.get(slug=payload['slug'])
        submission, new = AssessmentSubmission.objects.get_or_create(
            youth=youth,
            assessment=assessment,
            status=payload['status']
        )
        submission.data = payload
        submission.save()

        return HttpResponse()


class ExportView(LoginRequiredMixin, ListView):

    model = YoungPerson
    queryset = YoungPerson.objects.all()

    def get(self, request, *args, **kwargs):

        data = tablib.Dataset()
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

        queryset = self.queryset.filter(partner_organization=self.request.user.partner)

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
                line.address
            ]
            data.append(content)

        file_format = base_formats.XLS()
        response = HttpResponse(
            file_format.export_data(data),
            content_type='application/vnd.ms-excel',
        )
        response['Content-Disposition'] = 'attachment; filename=youth_list.xls'
        return response
