from rest_framework.generics import (
    ListAPIView, CreateAPIView, RetrieveAPIView,
    UpdateAPIView, RetrieveUpdateAPIView
)

from .serializers import *
from bankrecon.models import (
    Bank, BankAccount, Catatan
)


class BankAccountListApiView(ListAPIView):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer


class BankAccountDetailApiView(RetrieveAPIView):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'id'


class CatatanListApiView(ListAPIView):
    serializer_class = CatatanSerializer

    def get_queryset(self):
        queryset = Catatan.objects.filter(
            create_by = self.request.user, is_delete=False
        )[:15]
        return queryset

class CatatanCreateApiView(CreateAPIView):
    queryset = Catatan.objects.all()
    serializer_class = CatatanSerializer

    def get_serializer_context(self, *args, **kwargs):
        context = super().get_serializer_context(*args, **kwargs)
        context['user'] = self.request.user
        return context


class CatatanUpdateApiView(UpdateAPIView):
    serializer_class = CatatanDeletingSerializer
    lookup_url_kwarg = 'id'
    lookup_field = 'id'

    def get_queryset(self):
        queryset = Catatan.objects.filter(
            create_by = self.request.user
        )
        return queryset

