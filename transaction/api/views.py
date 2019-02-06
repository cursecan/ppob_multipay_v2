from rest_framework.generics import (
    ListAPIView, RetrieveAPIView,
    CreateAPIView
)

from .serializers import *
from transaction.models import InstanSale


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