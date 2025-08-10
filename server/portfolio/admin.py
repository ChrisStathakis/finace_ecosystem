from django.contrib import admin

# Register your models here.
from .models import UserTicker


@admin.register(UserTicker)
class UserTickerAdmin(admin.ModelAdmin):
    list_display = ['ticker', 'qty', "starting_investment"]