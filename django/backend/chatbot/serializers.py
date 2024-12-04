from rest_framework import serializers
from .models import TravelPlan

class TravelPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelPlan
        fields = ['id', 'destination', 'start_date', 'end_date', 'created_at']