
from rest_framework import serializers
from .models import (
    HouseHold,
    Child
)


class HouseHoldSerializer(serializers.ModelSerializer):

    class Meta:
        model = HouseHold
        fields = (
            'name',
            'barcode_number',
            'children',
        )


class ChildSerializer(serializers.ModelSerializer):

    child_id = serializers.CharField(source='id', read_only=True)
    student_first_name = serializers.CharField(source='first_name', read_only=True)
    student_father_name = serializers.CharField(source='father_name', read_only=True)
    student_last_name = serializers.CharField(source='last_name', read_only=True)
    student_full_name = serializers.CharField(source='full_name', read_only=True)
    student_mother_fullname = serializers.CharField(source='mother_fullname', read_only=True)
    student_sex = serializers.CharField(source='sex', read_only=True)
    student_birthday_year = serializers.CharField(source='birthday_year', read_only=True)
    student_birthday_month = serializers.CharField(source='birthday_month', read_only=True)
    student_birthday_day = serializers.CharField(source='birthday_day', read_only=True)
    student_birthday = serializers.CharField(source='birthday', read_only=True)
    student_phone = serializers.CharField(source='phone', read_only=True)
    student_phone_prefix = serializers.CharField(source='phone_prefix', read_only=True)
    student_id_number = serializers.CharField(source='id_number', read_only=True)
    student_id_type = serializers.CharField(source='id_type.id', read_only=True)
    student_nationality = serializers.CharField(source='nationality.id', read_only=True)
    student_mother_nationality = serializers.CharField(source='mother_nationality.id', read_only=True)
    student_address = serializers.CharField(source='address', read_only=True)

    class Meta:
        model = Child
        fields = (
            'child_id',
            'student_first_name',
            'student_father_name',
            'student_last_name',
            'student_full_name',
            'student_mother_fullname',
            'student_sex',
            'student_birthday_year',
            'student_birthday_month',
            'student_birthday_day',
            'student_birthday',
            'student_phone',
            'student_phone_prefix',
            'student_id_number',
            'student_id_type',
            'student_nationality',
            'student_mother_nationality',
            'student_address',
        )
