from django.shortcuts import render, HttpResponseRedirect, reverse, get_object_or_404
from django.views.generic import ListView

from .models import RssFeed
from .rss_helper import RssMachineLearning


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
    print('here!')
    instance = get_object_or_404(RssFeed, id=pk)
    rss_helper = RssMachineLearning()
    rss_helper.load_data('rss_component/enron1/spam/', 1)
    rss_helper.load_data('rss_component/enron1/ham/', 0)
    rss_helper.train_data()

    return render(request, 'rss_detail_view.html', context={"instance": instance})

def analysis_rss_view(request):
    RssFeed.analysis_rss_feed()
    return HttpResponseRedirect(reverse('rss:list'))


