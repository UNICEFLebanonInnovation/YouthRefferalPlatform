# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.views.generic import DetailView, ListView, RedirectView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets, mixins, permissions
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from dal import autocomplete
from django.db.models import Q

from .models import (
    Student,
)
from .serializers import (
    StudentSerializer,
)


class StudentViewSet(mixins.RetrieveModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):

    model = Student
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        qs = self.queryset
        if self.request.GET.get('barcode', None):
            qs = qs.filter(hh_barcode=self.request.GET.get('barcode', None))
        if self.request.GET.get('case_number', None):
            qs = qs.filter(id_number=self.request.GET.get('case_number', None))
        if self.request.GET.get('name', None):
            for term in self.request.GET.get('name', None).split():
                qs = qs.filter(
                    Q(first_name__contains=term) |
                    Q(father_name__contains=term) |
                    Q(last_name__contains=term) |
                    Q(id_number__contains=term)
                ).distinct()
        try:
            if self.request.GET.get('individual_number', None):
                qs = qs.filter(id_number=self.request.GET.get('individual_number', None))
        except Exception as ex:
            print ex.message
            return []

        return qs


class StudentSearchViewSet(mixins.RetrieveModelMixin,
                           mixins.ListModelMixin,
                           mixins.CreateModelMixin,
                           mixins.UpdateModelMixin,
                           viewsets.GenericViewSet):

    model = Student
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        if self.request.method in ["PATCH", "POST", "PUT"]:
            return self.queryset
        terms = self.request.GET.get('term', 0)
        school_type = self.request.GET.get('school_type', '2ndshift')
        user_school = self.request.user.school_id
        school = int(self.request.GET.get('school', 0))
        if terms:
            qs = self.queryset
            for term in terms.split():
                qs = qs.filter(
                    Q(first_name__contains=term) |
                    Q(father_name__contains=term) |
                    Q(last_name__contains=term) |
                    Q(id_number__contains=term)
                ).distinct()
            return qs


class StudentAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Student.objects.none()

        qs = Student.objects.all()

        if self.q:
            qs = Student.objects.filter(
                Q(first_name__istartswith=self.q) | Q(father_name__istartswith=self.q) |
                Q(last_name__istartswith=self.q) | Q(id_number__istartswith=self.q)
            )

        return qs
