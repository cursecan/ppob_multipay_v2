from rest_framework.generics import (
    ListAPIView, CreateAPIView
)

from .serializers import *
from bankrecon.models import (
    Bank, BankAccount, Catatan
)


class BankAccountListApiView(ListAPIView):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer


class CatatanListApiView(ListAPIView):
    serializer_class = CatatanSerializer

    def get_queryset(self):
        queryset = Catatan.objects.filter(
            create_by = self.request.user
        )[:15]
        return queryset

class CatatanCreateApiView(CreateAPIView):
    queryset = Catatan.objects.all()
    serializer_class = CatatanSerializer

    def get_serializer_context(self, *args, **kwargs):
        context = super().get_serializer_context(*args, **kwargs)
        context['user'] = self.request.user
        return context

