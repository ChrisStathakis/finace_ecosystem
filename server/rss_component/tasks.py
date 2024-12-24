from celery import shared_task

from .models import RssFeed


@shared_task
def refresh_rss():
    RssFeed.create_data()
    RssFeed.analysis_rss_feed()
    RssFeed.fetch_economist_data()
    
 