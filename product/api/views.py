from rest_framework.generics import (
    ListAPIView, RetrieveAPIView
)

from .serializers import *
from product.models import (
    Product, Group, Operator, Prefix
)


class ProductListApiView(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True, type_product='IN')
        operator = self.request.GET.get('ocode', None)
        group = self.request.GET.get('gcode', None)
        prefix = self.request.GET.get('prefix', None)

        if operator:
            queryset = queryset.filter(operator__code=operator)
        if group:
            queryset = queryset.filter(group__code=group)
        if prefix:
            queryset = queryset.filter(operator__prefix__prefix=prefix)

        return queryset


class PpobProductListApiView(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True, type_product='QU')
        operator = self.request.GET.get('ocode', None)
        group = self.request.GET.get('gcode', None)
        prefix = self.request.GET.get('prefix', None)

        if operator:
            queryset = queryset.filter(operator__code=operator)
        if group:
            queryset = queryset.filter(group__code=group)
        if prefix:
            queryset = queryset.filter(operator__prefix__prefix=prefix)

        return queryset


class ProductDetailApiView(RetrieveAPIView):
    serializer_class = ProductSerializer
    lookup_url_kwarg = 'id'
    queryset = Product.objects.filter(is_active=True)


class OperatorListApiView(ListAPIView):
    serializer_class = OperatorSerializer

    def get_queryset(self):
        queryset = Operator.objects.all()
        group = self.request.GET.get('gcode', None)

        if group:
            queryset = queryset.filter(group__code=group).distinct()
        
        return queryset
























