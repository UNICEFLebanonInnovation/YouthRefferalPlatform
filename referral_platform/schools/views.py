# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.views.generic import DetailView, ListView, RedirectView, UpdateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import viewsets, mixins, permissions
from braces.views import GroupRequiredMixin


from .models import (
    School,
    ClassRoom,
    Section,
)

from .serializers import (
    SchoolSerializer,
    ClassRoomSerializer,
    SectionSerializer,
)
from .forms import ProfileForm


class SchoolViewSet(mixins.ListModelMixin,
                    viewsets.GenericViewSet):

    model = School
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    permission_classes = (permissions.IsAuthenticated,)


class ClassRoomViewSet(mixins.ListModelMixin,
                       viewsets.GenericViewSet):

    model = ClassRoom
    queryset = ClassRoom.objects.all()
    serializer_class = ClassRoomSerializer
    permission_classes = (permissions.IsAuthenticated,)


class SectionViewSet(mixins.ListModelMixin,
                     viewsets.GenericViewSet):

    model = Section
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = (permissions.IsAuthenticated,)


class ProfileView(LoginRequiredMixin,
                  GroupRequiredMixin,
                  FormView):

    template_name = 'schools/profile.html'
    form_class = ProfileForm
    success_url = '/schools/profile/'
    group_required = [u"SCHOOL"]

    def get_context_data(self, **kwargs):
        # force_default_language(self.request)
        """Insert the form into the context dict."""
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        return super(ProfileView, self).get_context_data(**kwargs)

    def get_form(self, form_class=None):
        instance = School.objects.get(id=self.request.user.school_id)
        if self.request.method == "POST":
            return ProfileForm(self.request.POST, instance=instance)
        else:
            return ProfileForm(instance=instance)

    def form_valid(self, form):
        instance = School.objects.get(id=self.request.user.school_id)
        form.save(request=self.request, instance=instance)
        return super(ProfileView, self).form_valid(form)
