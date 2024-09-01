from django.contrib import admin

from .models import Ticker, TickerDataFrame, Tags
from import_export.admin import ImportExportModelAdmin
from portfolio.models import Portfolio, UserTicker


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin): pass


@admin.register(Ticker)
class TickerAdmin(ImportExportModelAdmin):
    list_display = ['id', 'title', 'ticker', 'simply_return', 'price']
    readonly_fields = ['simply_return']
    search_fields = ['title', ]
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


@admin.register(UserTicker)
class UserTickerAdmin(admin.ModelAdmin):
    pass


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    pass