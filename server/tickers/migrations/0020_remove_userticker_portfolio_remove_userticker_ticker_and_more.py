# Generated by Django 4.2 on 2024-08-31 23:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickers', '0019_ticker_ticker_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userticker',
            name='portfolio',
        ),
        migrations.RemoveField(
            model_name='userticker',
            name='ticker',
        ),
        migrations.DeleteModel(
            name='Portfolio',
        ),
        migrations.DeleteModel(
            name='UserTicker',
        ),
    ]
