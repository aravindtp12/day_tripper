from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TravelPlanSerializer
from .models import TravelPlan

# Create your views here.

class ChatbotView(APIView):
    def post(self, request):
        try:
            destination = request.data.get('destination')
            start_date = request.data.get('start_date')
            end_date = request.data.get('end_date')

            # Create travel plan
            travel_plan = TravelPlan.objects.create(
                destination=destination,
                start_date=start_date,
                end_date=end_date
            )

            # Return response
            return Response({
                'status': 'success',
                'message': f'Travel plan created for {destination}',
                'data': TravelPlanSerializer(travel_plan).data
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
