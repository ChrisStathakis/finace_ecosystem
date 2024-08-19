from django.shortcuts import render, HttpResponseRedirect, reverse, get_object_or_404
from django.views.generic import ListView

from .models import RssFeed



class RssFeedListView(ListView):
    model = RssFeed
    template_name = "rss_list.html"
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        return context


def refresh_tickers_view(request):
    RssFeed.create_data()
    return HttpResponseRedirect(reverse('rss:list'))


def rss_detail_view(request, pk):

    instance = get_object_or_404(RssFeed, id=pk)
    return render(request, 'rss_detail_view.html', context={"instance": instance})


def analysis_rss_view(request):
    RssFeed.analysis_rss_feed()
    return HttpResponseRedirect(reverse('rss:list'))


