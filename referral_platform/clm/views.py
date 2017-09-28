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
from django_tables2 import MultiTableMixin, RequestConfig, SingleTableView
from django_tables2.export.views import ExportMixin

from referral_platform.youth.models import YoungPerson
from .filters import BLNFilter
from .tables import BootstrapTable, CommonTable
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
        return YoungPerson.objects.all()


class YouthAddView(LoginRequiredMixin, CreateView):

    template_name = 'clm/bln_add.html'
    form_class = CommonForm
    model = YoungPerson
    success_url = '/youth/'

    # def get_initial(self):
    #     initial = super(YouthAddView, self).get_initial()
    #     data = []
    #     if self.request.GET.get('enrollment_id'):
    #         instance = BLN.objects.get(id=self.request.GET.get('enrollment_id'))
    #         data = BLNSerializer(instance).data
    #     if self.request.GET.get('student_outreach_child'):
    #         instance = Child.objects.get(id=int(self.request.GET.get('student_outreach_child')))
    #         data = ChildSerializer(instance).data
    #     initial = data
    #
    #     return initial
    #
    # def form_valid(self, form):
    #     form.save(self.request)
    #     return super(YouthAddView, self).form_valid(form)


class YouthEditView(LoginRequiredMixin, UpdateView):

    template_name = 'clm/bln_edit.html'
    form_class = CommonForm
    model = YoungPerson
    success_url = '/youth/'

    # def get_context_data(self, **kwargs):
    #     # force_default_language(self.request)
    #     """Insert the form into the context dict."""
    #     if 'form' not in kwargs:
    #         kwargs['form'] = self.get_form()
    #     return super(YouthEditView, self).get_context_data(**kwargs)

    # def get_form(self, form_class=None):
    #     instance = BLN.objects.get(id=self.kwargs['pk'])
    #     if self.request.method == "POST":
    #         return BLNForm(self.request.POST, instance=instance, request=self.request)
    #     else:
    #         data = BLNSerializer(instance).data
    #         data['student_nationality'] = data['student_nationality_id']
    #         return BLNForm(data, instance=instance, request=self.request)
    #
    # def form_valid(self, form):
    #     instance = BLN.objects.get(id=self.kwargs['pk'])
    #     form.save(request=self.request, instance=instance)
    #     return super(YouthEditView, self).form_valid(form)


class YouthAssessment(SingleObjectMixin, RedirectView):

    model = Assessment

    def get_redirect_url(self, *args, **kwargs):

        assessment = self.get_object()
        youth = YoungPerson.objects.get(number=self.request.GET.get('youth_id'))

        url = '{form}?d[form_slug]={slug}&d[youth_id]={id}&d[status]={status}&returnURL={callback}'.format(
            form = assessment.assessment_form,
            slug = assessment.slug,
            id = youth.number,
            status = self.request.GET.get('status'),
            callback = self.request.META.get('HTTP_REFERER', youth.get_absolute_url())
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
