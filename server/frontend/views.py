from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, reverse
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from tickers.models import Portfolio, Ticker, UserTicker, TickerDataFrame

from tickers.tasks import update_ticker_from_detail_page
from tickers.forms import PortfolioBaseForm, UserTickerForm
from rss_component.models import RssFeed


@login_required()
def homepage_view(request):
    # refresh_ticker_data.delay()
    # daily_update_data_task.delay()
    context = dict()
    tickers = Ticker.objects.all()
    context['total_earnings'] = Portfolio.my_query.total_earnings()
    context['simply_return'] = Portfolio.my_query.total_simply_return()
    context["tickers"] = tickers
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


@method_decorator(login_required, name='dispatch')
class PortfolioListView(ListView):
    model = Portfolio
    paginate_by = 20
    template_name = 'portfolio_list.html'

    def get_queryset(self):
        user = self.request.user
        return self.model.my_query.user_portfolios(user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PortfolioBaseForm(self.request.POST or None, initial={'user': self.request.user})
        return context


@method_decorator(login_required, name='dispatch')
class PortfolioDetailView(DetailView):
    model = Portfolio
    template_name = 'portfolio_detail_view.html'
    pk_url_kwarg = "port_id"

    def get_queryset(self):
        user = self.request.user
        return self.model.my_query.user_portfolios(user)

    def get_context_data(self, **kwargs):
        # refresh_portfolio_tickers.delay(self.object.id)
        context = super().get_context_data(**kwargs)
        context['tickers'] = Ticker.objects.all()[:20]
        context['my_tickers'] = UserTicker.objects.filter(portfolio=self.object)
        return context


@login_required
def create_portfolio_item_view(request, dk, pk):
    portfolio = get_object_or_404(Portfolio, id=dk)
    ticker = get_object_or_404(Ticker, id=pk)
    context = dict()
    context['form'] = form = UserTickerForm(request.POST or None, initial={
        'ticker': ticker,
        'portfolio': portfolio
    })

    context['page_title'] = f'Add {ticker} to {portfolio}'
    context['back_url'] = portfolio.get_edit_url()
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(portfolio.get_edit_url())
    return render(request, 'form.html', context)