from django.contrib import admin

from .models import  Portfolio, UserTicker
from import_export.admin import ImportExportModelAdmin


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin): pass


@admin.register(UserTicker)
class UserTickerAdmin(admin.ModelAdmin):
    pass