from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Profile

class ProfileList(APIView):
    def get(self, request):
        profiles = Profile.objects.all()
        data = []
        for profile in profiles:
            data.append({
                "id": profile.id,
                "name": profile.name,
                "bank_account": profile.bank_account,
                "bank_account_name": profile.bank_account_name,
                "owner": profile.owner.id,
            })
        return Response(data)


# class ProfileDetail(APIView):
#     def get(self, request, pk):
#         profile = Profile.objects.get(id=pk)
#         data = {
#             "id": profile.id,
#             "name": profile.name,
#             "bank_account": profile.bank_account,
#             "bank_account_name": profile.bank_account_name,
#             "owner": profile.owner.id,
#         }
#         return Response(data)
