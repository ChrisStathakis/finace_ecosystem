from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import RssFeed, RssFeedSerializer



class RssFeedListApiView(ListAPIView):
    queryset = RssFeed.objects.all()
    serializer_class = RssFeedSerializer
    permission_classes = [AllowAny, ]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['title', ]


    def get_queryset(self):
        ticker = self.request.query_params.get("ticker")
        if ticker:
            return self.queryset.filter(tickers__id=ticker)

        return super().get_queryset()



class RssFeedDetailApiView(RetrieveAPIView):
    queryset = RssFeed.objects.all()
    serializer_class = RssFeedSerializer
