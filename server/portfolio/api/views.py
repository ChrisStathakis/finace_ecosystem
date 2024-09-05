from rest_framework.generics import DestroyAPIView

from ..models import UserTicker

class UserTickerDeleteApiView(DestroyAPIView):
    serializer_class = ...


    def get_queryset(self):
        user = self.request.user
        return user.port.port_tickers.all()