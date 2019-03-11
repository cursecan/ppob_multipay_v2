from django.contrib.auth.models import User
from rest_framework.generics import (
    ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from .serializers import *
from userprofile.models import (
    Wallet, Profile
)


class UserListApiView(ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = User.objects.all()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(profile__agen=self.request.user)
        
        return queryset
    

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


class SignUpApiView(CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = CustomSignupSerializer
    permission_classes = [AllowAny]


class UpdateLimitApiView(UpdateAPIView):
    serializer_class = WalletSerializer
    lookup_url_kwarg = 'id'
    lookup_field = 'profile__guid'

    def get_queryset(self):
        queryset = Wallet.objects.all()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(profile__agen=self.request.user)
        return queryset

