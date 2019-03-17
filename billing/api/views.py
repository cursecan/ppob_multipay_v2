from rest_framework.generics import (
    ListAPIView, RetrieveAPIView
)
from django.db.models import F, Q

from .serializers import *
from billing.models import (
    BillingRecord, CommisionRecord
)

class BillingRecordListApiView(ListAPIView):
    queryset = BillingRecord.objects.all()
    serializer_class = BillingRecordSerializer


class BillingRecordTransactionApiListView(ListAPIView):
    serializer_class = BillingRecordSerializer

    def get_queryset(self):
        queryset = BillingRecord.objects.filter(
            sequence = 1
        ).filter(
            Q(instansale_trx__isnull=False) | Q(ppobsale_trx__isnull=False) 
        )

        if not self.request.user.is_superuser :
            if self.request.user.profile.user_type in [1,3]:
                queryset = queryset.filter(
                    user = self.request.user
                )
            else :
                queryset = queryset.filter(
                    user__profile__agen = self.request.user
                )
        return queryset


class BillingRecordTransactionDetailApiView(RetrieveAPIView):
    queryset = BillingRecord.objects.filter(
        sequence = 1
    ).filter(
        Q(instansale_trx__isnull=False) | Q(ppobsale_trx__isnull=False) 
    )
    serializer_class = BillingRecordSerializer
    lookup_url_kwarg = 'id'

