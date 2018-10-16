
from rest_framework import serializers
from .models import Exporter


class ExporterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Exporter
        fields = (
            'name',
        )
