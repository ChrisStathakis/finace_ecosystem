from django.contrib import admin

from .models import RssFeed
from .my_actions import update_tickers_on_rss_qs
# Register your models here.


@admin.register(RssFeed)
class RssFeedAdmin(admin.ModelAdmin):
    list_display = ["title", "is_analysed", "is_positive"]
    list_filter = ["is_analysed", "is_positive"]
    actions = [update_tickers_on_rss_qs, ]
    search_fields = ["title", ]

