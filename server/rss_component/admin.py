from django.contrib import admin

from .models import RssFeed
from .my_actions import update_tickers_on_rss_qs
# Register your models here.


@admin.action(description="DOWNLOAD NEW DATA")
def download_rss_action(modeladmin, request, queryset):
    RssFeed.create_data()


@admin.action(description="ANALYSE SELECTED RSS FEED")
def analyse_rss_action(modeladmin, request, queryset):
    RssFeed.analysis_rss_feed(queryset)


@admin.register(RssFeed)
class RssFeedAdmin(admin.ModelAdmin):
    list_display = ["title", "is_analysed", "is_positive"]
    list_filter = ["is_analysed", "is_positive"]
    actions = [update_tickers_on_rss_qs, ]
    search_fields = ["title", ]
    actions = [download_rss_action, analyse_rss_action, ]

