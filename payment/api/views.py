from rest_framework.generics import (
    ListAPIView, RetrieveAPIView
)

from payment.models import (
    Payment, LoanPayment
)
from .serializers import *


class PaymentListApiView(ListAPIView):
    serializer_class = PaymentSerializer

    def get_queryset(self):
        queryset = Payment.objects.all()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(user=self.request.user)
        return queryset