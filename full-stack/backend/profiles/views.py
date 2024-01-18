from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ProfileSerializer
from .permissions import IsOwnerOrReadOnly

from .models import Profile


class ProfileList(APIView):
    def get(self, request):
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True,
                                       context={'request': request})
        return Response(serializer.data)


class ProfileDetail(APIView):
    # This is for the django browsable API to display the fields
    serializer_class = ProfileSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_object(self, request, pk):
        try:
            profile = Profile.objects.get(pk=pk)
            self.check_object_permissions(request, profile)
            return profile

        except Profile.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        profile = self.get_object(request, pk)
        serializer = ProfileSerializer(profile, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        profile = self.get_object(request, pk)
        serializer = ProfileSerializer(profile, data=request.data,
                                       context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        profile = self.get_object(request, pk)
        profile.delete()
        return Response(status=204)

    def patch(self, request, pk):
        profile = self.get_object(request, pk)
        serializer = ProfileSerializer(profile, data=request.data,
                                       partial=True,
                                       context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
