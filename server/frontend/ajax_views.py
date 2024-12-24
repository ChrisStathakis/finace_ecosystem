from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.template.loader import render_to_string
from tickers.models import Ticker
from portfolio.models import Portfolio


@login_required
def search_tickers_json_view(request, pk):
    instance = get_object_or_404(Portfolio, id=pk)
    tickers = Ticker.filter_data(Ticker.objects.all(), request)
    data = dict()
    data['result'] = render_to_string('ajax/tickers_search_container.html',
                                       context={
                                           'tickers': tickers,
                                           'object': instance
                                       }
                                       )
    print(tickers)
    return JsonResponse(data)

