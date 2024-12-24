from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, reverse
from django.views.generic import ListView, CreateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from tickers.models import  Ticker, TickerDataFrame

from rss_component.models import RssFeed


def homepage_view(request):
    context = dict()
    context["tickers"] = Ticker.my_query.first_page_tickers()
    return render(request, 'index.html', context=context)


def update_ticker_portfolio_view(request, pk):
    instance = get_object_or_404(Ticker, id=pk)
    instance.save()
    return HttpResponseRedirect(redirect_to=instance.get_absolute_url())


