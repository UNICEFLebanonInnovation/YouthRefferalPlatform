# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.views.generic import DetailView, ListView, RedirectView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets, mixins, permissions
from dal import autocomplete
from django.db.models import Q
from .models import HouseHold, Child
from .serializers import HouseHoldSerializer, ChildSerializer


class HouseHoldViewSet(mixins.RetrieveModelMixin,
                       mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       mixins.UpdateModelMixin,
                       viewsets.GenericViewSet):

    model = HouseHold
    queryset = HouseHold.objects.all()
    serializer_class = HouseHoldSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        terms = self.request.GET.get('term', 0)
        if terms:
            qs = self.queryset
            for term in terms.split():
                qs = qs.filter(
                    Q(barcode_number=term) |
                    Q(children__barcode_number=term) |
                    Q(children__first_name__contains=term) |
                    Q(children__father_name__contains=term) |
                    Q(children__last_name__contains=term) |
                    Q(children__id_number__contains=term)
                ).distinct()
            return qs
        return self.queryset


class ChildViewSet(mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.UpdateModelMixin,
                   viewsets.GenericViewSet):

    model = Child
    queryset = Child.objects.all()
    serializer_class = ChildSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        terms = self.request.GET.get('term', 0)
        if terms:
            qs = self.queryset
            for term in terms.split():
                qs = qs.filter(
                    Q(barcode_subset__contains=term) |
                    Q(first_name__contains=term) |
                    Q(father_name__contains=term) |
                    Q(last_name__contains=term) |
                    Q(id_number__contains=term)
                ).distinct()
            return qs
        return self.queryset
