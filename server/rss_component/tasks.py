from celery import shared_task

from .models import RssFeed


@shared_task
def refresh_rss():
    qs = RssFeed.objects.filter(is_analysed=False)
    RssFeed.create_data()
    RssFeed.analysis_rss_feed(qs)
    RssFeed.fetch_economist_data()
    
 