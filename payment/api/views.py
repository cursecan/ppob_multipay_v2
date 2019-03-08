from rest_framework.generics import (
    ListAPIView, RetrieveAPIView, CreateAPIView
)

from payment.models import (
    Payment, LoanPayment, Transfer
)
from billing.models import LoanRecord

from .serializers import *


class PaymentListApiView(ListAPIView):
    serializer_class = PaymentSerializer

    def get_queryset(self):
        queryset = Payment.objects.all()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(user=self.request.user)
        return queryset


class LoanPaymentFlagApiView(CreateAPIView):
    serializer_class = LoanPaymentSerializer
    queryset = LoanPayment.objects.all()

    def get_serializer_context(self, *args, **kwargs):
        context = super().get_serializer_context(*args, **kwargs)
        context['user'] = self.request.user
        return context


class TransferCreateApiView(CreateAPIView):
    serializer_class = TransferSerializer
    queryset = Transfer.objects.all()

    def get_serializer_context(self, *args, **kwargs):
        context = super().get_serializer_context(*args, **kwargs)
        context['sender'] = self.request.user
        return context