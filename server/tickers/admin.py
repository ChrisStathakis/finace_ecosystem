from django.contrib import admin

from .models import Ticker, TickerDataFrame, Tags
from import_export.admin import ImportExportModelAdmin


@admin.action(description="SOFT UPDATE")
def ticker_soft_update_action(modeladmin, request, queryset):
    for ticker in queryset:
        ticker.soft_update()


@admin.action(description="HARD UPDATE")
def ticker_test_hard_update_action(modeladmin, request, queryset):
    for ticker in queryset:
        print("ticker queryset", ticker)
        ticker.hard_update()


@admin.action(description="SENTIMENTAL ANALYSIS ACTION")
def ticker_sentimental_analysis_action(modeladmin, request, queryset):
    for ticker in queryset:
        ticker.sentimental_analysis_update()


@admin.register(Ticker)
class TickerAdmin(ImportExportModelAdmin):
    list_display = ['id', 'title', 'ticker', 'simply_return', 'price']
    readonly_fields = ['simply_return']
    search_fields = ['title', ]
    actions = [ticker_test_hard_update_action, ticker_soft_update_action,
               ticker_sentimental_analysis_action
               ]
    fieldsets = [
        (
            'General',
            {
                "fields": [('title', 'ticker'),
                           ("wikipedia_url", ),
                           ]
            }
        ),
        (
            'Values',
            {
                "fields": [('simply_return', 'price'),
                           ('date_predict', 'prediction')
                           ]
            }
        )

    ]


@admin.register(TickerDataFrame)
class TickerDataFrameAdmin(admin.ModelAdmin):
    list_display = ['date', 'close', 'ticker']
    list_filter = ['ticker', ]


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    pass