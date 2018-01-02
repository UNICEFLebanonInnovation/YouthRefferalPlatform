# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import json

from django.views.generic import ListView, FormView, TemplateView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import RedirectView
from django_filters.views import FilterView
from django_tables2 import RequestConfig, SingleTableView
from django_tables2.export.views import ExportMixin
from referral_platform.youth.models import YoungPerson
from .filters import BLNFilter
from .tables import CommonTable
from .forms import CommonForm
from .models import Assessment, AssessmentSubmission



class YouthListView(LoginRequiredMixin,
                    FilterView,
                    ExportMixin,
                    SingleTableView,
                    RequestConfig):
    table_class = CommonTable
    model = YoungPerson
    template_name = 'clm/bln_list.html'

    filterset_class = BLNFilter

    def get_queryset(self):
        return YoungPerson.objects.filter(partner_organization=self.request.user.partner)


class YouthAddView(LoginRequiredMixin, CreateView):
    template_name = 'clm/bln_add.html'
    form_class = CommonForm
    model = YoungPerson
    success_url = '/youth/'

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

        return super(YouthAddView, self).form_valid(form)


class YouthEditView(LoginRequiredMixin, UpdateView):
    template_name = 'clm/bln_edit.html'
    form_class = CommonForm
    model = YoungPerson
    success_url = '/youth/'

    def get_initial(self):
        data = dict()
        if self.request.user.partner:
            data['partner_locations'] = self.request.user.partner.locations.all()
            data['partner'] = self.request.user.partner
        initial = data
        return initial

    def form_valid(self, form):
        form.save(self.request)
        return super(YouthEditView, self).form_valid(form)


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
