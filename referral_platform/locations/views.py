from django.shortcuts import render

# Create your views here.
from __future__ import absolute_import, unicode_literals
from django.views.generic import ListView, FormView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin




class ExecSequenceView(LoginRequiredMixin, TemplateView):

    template_name = 'initiatives/execs.html'

    def get_context_data(self, **kwargs):
        from django.db import connection

        cursor = connection.cursor()
        cursor1 = connection.cursor()

        cursor.execute("SELECT setval('locations_location_id_seq', (SELECT max(id) FROM locations_location))")
        cursor1.execute("SELECT setval('locations_locationtype_id_seq', (SELECT max(id) FROM locations_locationtype))")

        return {
            'result1': cursor.fetchall(),
            'result2': cursor1.fetchall(),
        }
