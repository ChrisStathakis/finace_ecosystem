from django.contrib import admin

from .models import Ticker, TickerDataFrame
from import_export.admin import ImportExportModelAdmin





@admin.register(Ticker)
class TickerAdmin(ImportExportModelAdmin):
    list_display = ['id', 'title', 'ticker', 'simply_return', 'price']
    readonly_fields = ['simply_return']
    search_fields = ['title', ]
    fieldsets = [
        (
            'General',
            {
                "fields": [('title', 'ticker'), ]
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

