from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required


from .models import Portfolio, UserTicker
from .forms import UserTickerForm
from tickers.models import Ticker


@login_required
def portfolio_view(request):
    user = request.user
    portfolio, created = Portfolio.objects.get_or_create(user=user)
    context = dict()
    context['tickers'] = Ticker.objects.all()[:20]
    context['my_tickers'] = UserTicker.objects.filter(portfolio=portfolio)
    context["object"] = portfolio
    return render(request, "portfolio_detail_view.html", context)



@login_required
def create_portfolio_item_view(request, pk, dk):
    portfolio = get_object_or_404(Portfolio, id=pk)
    ticker = get_object_or_404(Ticker, id=dk)
    context = dict()
    context['form'] = form = UserTickerForm(request.POST or None, initial={
        'ticker': ticker,
        'portfolio': portfolio
    })

    context['page_title'] = f'Add {ticker} to {portfolio}'
    context['back_url'] = reverse("port:home")
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse("port:home"))
    return render(request, 'form.html', context)