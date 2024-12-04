import sys
import logging

# Add the parent directory to Python path
sys.path.append("/Users/aravindmanoj/day_tripper/")

from agents.reddit.reddit import RedditAgent
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TravelPlanSerializer
from .models import TravelPlan

logger = logging.getLogger(__name__)

# Create your views here.

class ChatbotView(APIView):
    def post(self, request):
        try:
            destination = request.data.get('destination')
            start_date = request.data.get('start_date')
            end_date = request.data.get('end_date')

            logger.info(f"Received request for destination: {destination}")

            # Create travel plan
            travel_plan = TravelPlan.objects.create(
                destination=destination,
                start_date=start_date,
                end_date=end_date
            )

            # Generate recommendations using RedditAgent
            reddit_agent = RedditAgent(destination)
            recommendations = reddit_agent.generate_recommendations()
            
            logger.info(f"Generated recommendations: {recommendations.content}")

            response_data = {
                'status': 'success',
                'message': f'Travel plan created for {destination}',
                'data': TravelPlanSerializer(travel_plan).data,
                'recommendations': recommendations.content
            }
            
            logger.info(f"Sending response: {response_data}")
            
            return Response(response_data, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f"Error occurred: {str(e)}")
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
