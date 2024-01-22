from django.shortcuts import get_object_or_404
from .serializers import ChurchesAndCostPurposesSerializer
from rest_framework.decorators import APIView
from rest_framework.response import Response
from .models import Church


class ChurchesAndCostPurposes(APIView):
    def get(self, request):
        church_name = request.query_params.get('church')
        church = get_object_or_404(Church, name=church_name)
        serializer = ChurchesAndCostPurposesSerializer(church)
        return Response(serializer.data)
