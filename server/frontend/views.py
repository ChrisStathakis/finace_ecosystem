from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, reverse
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from portfolio.models import Portfolio
from tickers.models import  Ticker, TickerDataFrame
from portfolio.models import UserTicker, Portfolio
from strategies.models import TickerAnalysis
from tickers.tasks import update_ticker_from_detail_page
from tickers.forms import PortfolioBaseForm, UserTickerForm
from rss_component.models import RssFeed


def homepage_view(request):
    context = dict()
    context["tickers"] = Ticker.my_query.first_page_tickers()
    return render(request, 'index.html', context=context)


class TickerListView(ListView):
    model = Ticker
    paginate_by = 50
    template_name = "tickers_list.html"

    def get_queryset(self):
        return Ticker.filter_data(Ticker.objects.all(), self.request)


def ticker_detail_view(request, pk):
    instance = get_object_or_404(Ticker, id=pk)
    # instance.save()
    # instance.predict_next_days(days=1)
    feed = RssFeed.objects.filter(tickers=instance)
    prices = TickerDataFrame.objects.filter(ticker=instance)[:30]
    prices_chart = [[price.date.split(" ")[0], price.close] for price in reversed(prices)]


    return render(
                request,
                'ticker_detail.html',
                context={
                    "instance": instance,
                    "feed": feed,
                    "prices": prices,
                    "prices_chart": prices_chart
                }
                )


def update_ticker_portfolio_view(request, pk):
    instance = get_object_or_404(Ticker, id=pk)
    instance.save()
    return HttpResponseRedirect(redirect_to=instance.get_absolute_url())


