
from rest_framework import serializers
from .models import Registration, AssessmentSubmission


class AssessmentSubmissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = AssessmentSubmission
        fields = '__all__'


class RegistrationSerializer(serializers.ModelSerializer):

    governorate_id = serializers.IntegerField(source='governorate.id', required=False)

    youth_bayanati_ID = serializers.CharField(source='youth.bayanati_ID', required=False)
    youth_first_name = serializers.CharField(source='youth.first_name')
    youth_father_name = serializers.CharField(source='youth.father_name')
    youth_last_name = serializers.CharField(source='youth.last_name')
    youth_sex = serializers.CharField(source='youth.sex')
    youth_birthday_year = serializers.CharField(source='youth.birthday_year')
    youth_birthday_month = serializers.CharField(source='youth.birthday_month')
    youth_birthday_day = serializers.CharField(source='youth.birthday_day')

    youth_nationality = serializers.CharField(source='youth.nationality', required=False)
    youth_address = serializers.CharField(source='youth.address', required=False)
    youth_marital_status = serializers.CharField(source='youth.marital_status', required=False)

    youth_nationality_id = serializers.CharField(source='youth.nationality.id', read_only=True)
    csrfmiddlewaretoken = serializers.IntegerField(source='owner.id', read_only=True)
    save = serializers.IntegerField(source='owner.id', read_only=True)

    def create(self, validated_data):
        from referral_platform.youth.serializers import YoungPersonSerializer
        from referral_platform.youth.models import YoungPerson

        youth_data = validated_data.pop('youth', None)

        youth_serializer = YoungPersonSerializer(data=youth_data)
        youth_serializer.is_valid(raise_exception=True)
        youth_serializer.instance = youth_serializer.save()

        try:
            validated_data['youth_id'] = youth_serializer.instance.id
            instance = Registration.objects.create(**validated_data)
            instance.save()

        except Exception as ex:
            raise serializers.ValidationError({'Enrollment instance': ex.message})

        return instance

    def update(self, instance, validated_data):

        youth_data = validated_data.pop('youth', None)

        if youth_data:
            from referral_platform.youth.serializers import YoungPersonSerializer
            youth_serializer = YoungPersonSerializer(instance.youth, data=youth_data)
            youth_serializer.is_valid(raise_exception=True)
            youth_serializer.instance = youth_serializer.save()

        try:

            for key in validated_data:
                if hasattr(instance, key):
                    setattr(instance, key, validated_data[key])

            instance.save()

        except Exception as ex:
            raise serializers.ValidationError({'Enrollment instance': ex.message})

        return instance

    class Meta:
        model = Registration
        fields = (
            'id',
            'governorate',
            'location',
            'center',
            'trainer',
            'youth_bayanati_ID',
            'youth_first_name',
            'youth_father_name',
            'youth_last_name',
            'youth_sex',
            'youth_birthday_year',
            'youth_birthday_month',
            'youth_birthday_day',
            'youth_nationality',
            'youth_address',
            'youth_marital_status',
            'youth_nationality_id',
            'governorate_id',
            'csrfmiddlewaretoken',
            'save',
        )
