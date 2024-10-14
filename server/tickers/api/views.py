from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.reverse import reverse

from .serializers import (TickerSerializer, TickerDataFrameSerializer, TickerPredictionSerializer,
                          TickerCreateSerializer
                          )
from ..models import Ticker, TickerDataFrame


@api_view(['GET'])
def ticker_homepage_api_view(request, format=None):
    return Response({
        'tickers': reverse('api_tickers:tickers_list', request=request, format=format),
        "ticker_dataframe": reverse("api_tickers:ticker_dataframe", request=request, format=format),
        "create": reverse("api_tickers:ticker_create", request=request, format=format)

    })


class TickerCreateApiView(CreateAPIView):
    serializer_class = TickerCreateSerializer
    permission_classes = [IsAuthenticated, ]


class TickerListApiView(ListAPIView):
    queryset = Ticker.objects.all()
    serializer_class = TickerSerializer
    permission_classes = [AllowAny,]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', "ticker"]
    ordering_fields = ["simply_return", "title"]


class TickerRetrieveApiView(RetrieveAPIView):
    queryset = Ticker.objects.all()
    serializer_class = TickerSerializer
    permission_classes = [AllowAny, ]


class TickerPredictionsApiView(RetrieveAPIView):
    queryset = Ticker.objects.all()
    serializer_class = TickerPredictionSerializer


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