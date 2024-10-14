from rest_framework.generics import (DestroyAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView,
                                     RetrieveAPIView
                                     )
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsAuthenticatedCustom
from ..models import UserTicker, Portfolio
from .serializers import UserTickerSerializer, PortfolioSerializer, UserTickerBaseSerializer, UserTickerEditSerializer


@api_view(['GET'])
def ticker_homepage_api_view(request, format=None):
    return Response({
        "portfolios": reverse("api_port:list", request=request, format=format),
        "user_ticker_list": reverse("api_port:user_ticker_list", request=request, format=format),
        "efficient_frontier": reverse("api_port:efficient_frontier", request = request, format = format),
    })


class PortfolioListApiView(ListCreateAPIView):
    serializer_class = PortfolioSerializer
    permission_classes = [IsAuthenticatedCustom, ]

    def get_queryset(self):
        return Portfolio.objects.filter(user=self.request.user)


class PortfolioUpdateRetrieveApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = PortfolioSerializer
    permission_classes = [IsAuthenticatedCustom, ]

    def get_queryset(self):
        return Portfolio.objects.filter(user=self.request.user)


class UserTickerListApiView(ListCreateAPIView):
    serializer_class = UserTickerBaseSerializer
    permission_classes = [IsAuthenticatedCustom, ]
    filter_backends = [DjangoFilterBackend, ]
    filterset_fields = ['portfolio', "is_sell"]

    def get_queryset(self):
        return UserTicker.objects.filter(portfolio__user=self.request.user)


class UserTickerCreateApiView(CreateAPIView):
    serializer_class = UserTickerEditSerializer
    permission_classes = [IsAuthenticatedCustom, ]


class UserTickerRetrieveApiView(RetrieveAPIView):
    queryset = UserTicker.objects.all()
    serializer_class = UserTickerBaseSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        qs = UserTicker.objects.filter(portfolio__user=self.request.user)
        return qs


class UserTickerUpdateDeleteApiView(RetrieveUpdateDestroyAPIView):
    queryset = UserTicker.objects.all()
    serializer_class = UserTickerEditSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        qs = UserTicker.objects.filter(portfolio__user=self.request.user)
        return qs


class UserTickerDeleteApiView(DestroyAPIView):
    serializer_class = UserTickerSerializer

    def get_queryset(self):
        user = self.request.user
        return user.port.port_tickers.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Obj deleted"})


@api_view(["GET"])
def efficient_frontier_view(request, format=None):
    user = request.user
    if not user.is_authenticated:
        return Response({'message': "You have to login"})
    portfolios = Portfolio.objects.filter(user=user)
    results = dict()
    for port in portfolios:
        results[f"{port.title}"] = port.efficient_frontier()
    print("results",  results)
    return Response({"portfolios": results})