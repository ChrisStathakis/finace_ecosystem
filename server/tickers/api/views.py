from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.reverse import reverse

from .serializers import TickerSerializer, PortfolioSerializer, UserTickerBaseSerializer, TickerDataFrameSerializer
from ..models import Ticker, Portfolio, UserTicker, TickerDataFrame
from .permissions import IsAuthenticatedCustom

@api_view(['GET'])
def ticker_homepage_api_view(request, format=None):
    return Response({
        'tickers': reverse('api_tickers:tickers_list', request=request, format=format),
        "portfolios": reverse("api_tickers:portfolio_list", request=request, format=format),
        "ticker_dataframe": reverse("api_tickers:ticker_dataframe", request=request, format=format),

    })


class PortfolioListApiView(ListCreateAPIView):
    serializer_class = PortfolioSerializer
    permission_classes = [IsAuthenticatedCustom, ]

    def get_queryset(self):
        return Portfolio.objects.filter(user=self.request.user)


class PortfolioUpdateRetrieveApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = PortfolioSerializer

    def get_queryset(self):
        user = self.request.user
        if user:
            return Portfolio.objects.filter(user=user)
        return Portfolio.objects.none()


class TickerListApiView(ListAPIView):
    queryset = Ticker.objects.all()
    serializer_class = TickerSerializer
    permission_classes = [AllowAny,]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['title', "ticker"]


class TickerRetrieveApiView(RetrieveAPIView):
    queryset = Ticker.objects.all()
    serializer_class = TickerSerializer
    permission_classes = [AllowAny, ]


class TickerDataFrameListApiView(ListAPIView):
    queryset = TickerDataFrame.objects.all()
    serializer_class = TickerDataFrameSerializer
    permission_classes = [AllowAny, ]
    

    def get_queryset(self):
        qs = self.queryset
        ticker = self.request.query_params.get("ticker")
        if ticker:
            qs = qs.filter(ticker__id=ticker)
        return qs