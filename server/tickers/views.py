from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, reverse
from django.views.generic import ListView, CreateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import Ticker, TickerDataFrame
from .ticker_helper import TickerHelper
from .forms import TickerForm


class TickerListView(ListView):
    model = Ticker
    paginate_by = 50
    template_name = "tickers_list.html"

    def get_queryset(self):
        return Ticker.filter_data(Ticker.objects.all(), self.request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_tickers = self.model.objects.all().count()
        context['total_tickers'] = total_tickers
        return context


def ticker_detail_view(request, pk):
    instance = get_object_or_404(Ticker, id=pk)
    # instance.save()
    # instance.predict_next_days(days=1)
    feed = instance.rss.all()
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


def ticker_refresh_view(request, pk: int):
    # hard update to ticker data, this view should be hidden from public
    instance: Ticker = get_object_or_404(Ticker, id=pk)
    instance.wikipedia_url = instance.find_wikipedia_url()
    instance.update_ticker_data()
    instance.create_tags()
    instance.save()
    instance.create_ticker_database()
    return HttpResponseRedirect(instance.get_absolute_url())


@method_decorator(login_required, name="dispatch")
class CreateTickerView(CreateView):
    model = Ticker
    template_name = "ticker_form.html"
    form_class = TickerForm
    
    def get_success_url(self):
        return self.obj.get_absolute_url()

    def form_valid(self, form):
        self.obj = form.save()
        return super().form_valid(form)


def initial_data_view(request):
    Ticker.create_tickers()

    return render(request, "initial_data.html")


def ticker_play_area_view(request, pk):
    instance = get_object_or_404(Ticker, id=pk)
    helper = TickerHelper(ticker=instance, market='^GSPC')
    helper.analyze_ticker_wiki()
    return render(request, "play_area.html")