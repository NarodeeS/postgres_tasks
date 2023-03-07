from rest_framework import serializers

from .models import DatabaseInfo


class DatabaseInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatabaseInfo
        fields = '__all__'
