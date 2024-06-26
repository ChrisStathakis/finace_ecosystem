from django.contrib import admin

from .models import RssFeed, Ticker
from .rss_analyzer import RssAnalyzer


@admin.action(description="Update Tickers on Rss qs")
def update_tickers_on_rss_qs(modeladmin, request, queryset):
    for rss_feed in queryset:
        rss_feed.rss_find_ticker()