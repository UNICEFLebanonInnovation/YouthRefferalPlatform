from __future__ import unicode_literals, absolute_import, division

from django.utils.translation import ugettext as _
from django import forms
from referral_platform.students.models import (
    Student
)
from referral_platform.locations.models import Location
from referral_platform.schools.models import School


class StudentEnrollmentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(StudentEnrollmentForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Student
        fields = (
            'first_name',
            'father_name',
            'last_name',
            'mother_fullname',
            'sex',
            'birthday_year',
            'birthday_month',
            'birthday_day',
            'nationality',
            'mother_nationality',
            'id_type',
            'id_number',
            'phone',
            'phone_prefix',
            'address',
            'number',
        )
