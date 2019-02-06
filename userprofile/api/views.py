from django.contrib.auth.models import User
from rest_framework.generics import (
    ListAPIView, RetrieveAPIView
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import *
from userprofile.models import (
    Wallet, Profile
)


class UserListApiView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    

class UserDetailApiView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_url_kwarg = 'id'
    

class GetMeApiView(APIView):
    def get(self, request, *args, **kwargs):
        serializers = UserSerializer(request.user)
        return Response(serializers.data)


class WalletListApiView(ListAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer


