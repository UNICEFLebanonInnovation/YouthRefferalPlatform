
import datetime
import tempfile

import tablib

from django.utils.translation import ugettext as _
from import_export.formats import base_formats

from referral_platform.registrations.models import Registration, AssessmentSubmission


class RegistrationFormat(base_formats.XLS):

    def get_title(self):
        return 'Registrations'

    def export_data(self, dataset):

        headers = [
            _('Unique number'),
            _('First name'),
            _('Father name'),
            _('Last name'),
            _('Governorate'),
            _('Trainer'),
            _('Location'),
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
        ]

        if dataset.csv != '':

            submission_set = Registration.objects.filter(id__in=dataset['ID'])
            book = tablib.Databook()

            data2 = tablib.Dataset()
            data2.title = "Registration"
            data2.headers = headers

            for registry in submission_set:
                content = []
                youth = registry.youth
                content = [
                    youth.number,
                    youth.first_name,
                    youth.father_name,
                    youth.last_name,
                    registry.governorate.name if registry.governorate else '',
                    registry.trainer,
                    registry.location,
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
                ]
                data2.append(content)

            book.add_sheet(data2)
        else:
            data2 = tablib.Dataset(headers=headers)

        file_format = base_formats.XLS()
        data = file_format.export_data(data2)
        return data


class RegistrationAssessmentFormat(base_formats.XLS):

    def get_title(self):
        return 'Registration Assessment'

    def export_data(self, dataset):

        headers = [
            _('Unique number'),
            _('First name'),
            _('Father name'),
            _('Last name'),
            _('Governorate'),
            _('Trainer'),
            _('Location'),
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
        ]

        if dataset.csv != '':

            submission_set = AssessmentSubmission.objects.filter(registration__id__in=dataset['ID'])
            book = tablib.Databook()

            data2 = tablib.Dataset()
            data2.title = "Registration Assessment"
            data2.headers = headers

            for line2 in submission_set:
                content = []
                if ('slug' in line2.data and line2.data["slug"] == 'registration') or line2.data['__version__'] == 'vhi7pe6TonRqiDdWwAbnMS':
                    youth = line2.youth
                    registry = line2.registration
                    content = [
                        youth.number,
                        youth.first_name,
                        youth.father_name,
                        youth.last_name,
                        registry.governorate.name if registry.governorate else '',
                        registry.trainer,
                        registry.location,
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
                    ]
                    data2.append(content)

            book.add_sheet(data2)
        else:
            data2 = tablib.Dataset(headers=headers)

        file_format = base_formats.XLS()
        data = file_format.export_data(data2)
        return data
