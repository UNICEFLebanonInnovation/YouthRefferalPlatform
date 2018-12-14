from __future__ import absolute_import, unicode_literals

from django.views.generic import TemplateView, FormView

from django.contrib.auth.mixins import LoginRequiredMixin

from referral_platform.users.views import UserRegisteredMixin

from .forms import YouthLedInitiativePlanningForm
from .models import YouthLedInitiative, YoungPerson


class YouthInitiativeView(UserRegisteredMixin, FormView):

    template_name = 'courses/community/initiative.html'
    form_class = YouthLedInitiativePlanningForm


class AddView(LoginRequiredMixin, FormView):

    template_name = 'initiatives/form.html'
    model = YouthLedInitiative
    success_url = '/initiatives/form.html'
    form_class = YouthLedInitiativePlanningForm

    def get_success_url(self):
        if self.request.POST.get('save_add_another', None):
            del self.request.session['instance_id']
            return '/initiatives/add/'
        # if self.request.POST.get('save_and_continue', None):
        #     return '/initiatives/edit/' + str(self.request.session.get('instance_id')) + '/'
        return self.success_url

    def get_initial(self):
        # force_default_language(self.request, 'ar-ar')
        data = dict()
        if self.request.user.partner:
            data['partner_locations'] = self.request.user.partner.locations.all()
            data['partner_organization'] = self.request.user.partner
            data['members'] = YoungPerson.objects.filter(partner_organization=data['partner_organization'])

        # if self.request.GET.get('youth_id'):
        #         instance = YoungPerson.objects.get(id=self.request.GET.get('youth_id'))
        #         data['youth_id'] = instance.id
        #         data['youth_first_name'] = instance.first_name
        #         data['youth_father_name'] = instance.father_name
        #         data['youth_last_name'] = instance.last_name
        #         data['youth_birthday_day'] = instance.birthday_day
        #         data['youth_birthday_month'] = instance.birthday_month
        #         data['youth_birthday_year'] = instance.birthday_year
        #         data['youth_sex'] = instance.sex
        #         data['youth_nationality'] = instance.nationality_id
        #         data['youth_marital_status'] = instance.marital_status

        initial = data
        return initial

    def form_valid(self, form):
        form.save(request=self.request)
        return super(AddView, self).form_valid(form)
