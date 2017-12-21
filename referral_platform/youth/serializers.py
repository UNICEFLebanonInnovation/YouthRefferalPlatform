
import json

from rest_framework import serializers
from .models import YoungPerson


class YoungPersonSerializer(serializers.ModelSerializer):

    class Meta:
        model = YoungPerson
        fields = '__all__'
