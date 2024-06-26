from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(['GET'])
def homepage_api_view(request, format=None):
    return Response({
        'tickers_homepage': reverse('api_tickers:home', request=request, format=format)
    })