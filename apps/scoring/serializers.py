from rest_framework import serializers
from .models import CreditScore

class CreditScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditScore
        fields = '__all__'

class ScoreRequestSerializer(serializers.Serializer):
    application_id = serializers.UUIDField()
