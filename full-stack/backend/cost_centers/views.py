from django.shortcuts import get_object_or_404
from .serializers import ChurchDetailsSerializer
from .serializers import ChurchListSerializer
from rest_framework.decorators import APIView
from rest_framework.response import Response
from .models import Church


class ChurchDetails(APIView):
    def get(self, request):
        church_name = request.query_params.get('church')
        church = get_object_or_404(Church,
                                   short_name=church_name)
        serializer = ChurchDetailsSerializer(church)
        return Response(serializer.data)


class ChurchList(APIView):
    def get(self, request):
        churches = Church.objects.all()
        serializer = ChurchListSerializer(churches, many=True)
        return Response(serializer.data)
