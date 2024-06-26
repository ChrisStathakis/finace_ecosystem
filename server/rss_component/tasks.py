from celery import shared_task

from .models import RssFeed


@shared_task
def refresh_rss():
    RssFeed.analysis_rss_feed()
    
 