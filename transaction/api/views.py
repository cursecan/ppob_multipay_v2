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


# Create API Instan Sale
class InstanSaleCreateApiView(CreateAPIView):
    queryset = InstanSale.objects.all()
    serializer_class = InstanSaleCustomSerializer

    def get_serializer_context(self, *args, **kwargs):
        context = super().get_serializer_context(*args, **kwargs)
        context['user'] = self.request.user
        return context


# Create API Inquery PPOB
class PpobInqueryApiView(CreateAPIView):
    queryset = PpobSale.objects.all()
    serializer_class = PpobInquerySerializer

    def get_serializer_context(self, *args, **kwargs):
        context = super().get_serializer_context(*args, **kwargs)
        context['user'] = self.request.user
        return context


# Create API Sale PPOB
class PpobSaleCreateApiView(CreateAPIView):
    queryset = PpobSale.objects.all()
    serializer_class = PpobSaleCustomSerializer

    def get_serializer_context(self, *args, **kwargs):
        context = super().get_serializer_context(*args, **kwargs)
        context['user'] = self.request.user
        return context