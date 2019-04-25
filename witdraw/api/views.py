from rest_framework.generics import (
    CreateAPIView, ListAPIView
)

from witdraw.models import Witdraw
from .serializers import WitdrawSerializer

class WitdrawApiCreateView(CreateAPIView):
    queryset = Witdraw.objects.all()
    serializer_class = WitdrawSerializer

    def get_serializer_context(self, *args, **kwargs):
        context = super(WitdrawApiCreateView, self).get_serializer_context(*args, **kwargs)
        context['user'] = self.request.user
        return context