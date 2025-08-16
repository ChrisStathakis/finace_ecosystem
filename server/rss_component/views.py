from django.shortcuts import render, HttpResponseRedirect, reverse, get_object_or_404
from django.views.generic import ListView

from .models import RssFeed
from .rss_analyzer import RssAnalyzer


class RssFeedListView(ListView):
    model = RssFeed
    template_name = "rss_list.html"
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        RssFeed.fetch_xml_website()
        return context


def rss_detail_view(request, pk):
    instance: RssFeed = get_object_or_404(RssFeed, id=pk)
    analyzer = RssAnalyzer()
    result = analyzer.llm_check_if_positive(instance.title)
    return render(request, 'rss_detail_view.html', context={"instance": instance})





