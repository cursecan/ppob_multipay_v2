from rest_framework.generics import (
    ListAPIView, RetrieveAPIView,
    CreateAPIView
)
from rest_framework.views import APIView

from .serializers import *
from transaction.models import (
    InstanSale, PpobSale
)


class InstanSaleListApiView(ListAPIView):
    queryset = InstanSale.objects.all()
    serializer_class = InstanSaleCustomSerializer


class InstanSaleCreateApiView(CreateAPIView):
    queryset = InstanSale.objects.all()
    serializer_class = InstanSaleCustomSerializer

    def get_serializer_context(self, *args, **kwargs):
        context = super().get_serializer_context(*args, **kwargs)
        context['user'] = self.request.user
        return context


class PpobInqueryApiView(CreateAPIView):
    queryset = PpobSale.objects.all()
    serializer_class = PpobInquerySerializer

    def get_serializer_context(self, *args, **kwargs):
        context = super().get_serializer_context(*args, **kwargs)
        context['user'] = self.request.user
        return context


class PpobSaleCreateApiView(CreateAPIView):
    queryset = PpobSale.objects.all()
    serializer_class = PpobSaleCustomSerializer

    def get_serializer_context(self, *args, **kwargs):
        context = super().get_serializer_context(*args, **kwargs)
        context['user'] = self.request.user
        return context