from .serializers import ChurchesAndCostPurposesSerializer
from rest_framework.decorators import APIView
from rest_framework.response import Response
from .models import Church


class ChurchesAndCostPurposes(APIView):
    def get(self, request):
        churches = Church.objects.all()
        serializer = ChurchesAndCostPurposesSerializer(churches, many=True)
        return Response(serializer.data)
