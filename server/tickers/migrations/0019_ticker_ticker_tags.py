# Generated by Django 4.2 on 2024-08-19 00:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickers', '0018_ticker_wikipedia_url_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticker',
            name='ticker_tags',
            field=models.ManyToManyField(to='tickers.tags'),
        ),
    ]
