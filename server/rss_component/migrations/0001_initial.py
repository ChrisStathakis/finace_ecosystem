# Generated by Django 4.2 on 2024-03-04 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tickers', '0010_alter_ticker_indices_alter_userticker_portfolio'),
    ]

    operations = [
        migrations.CreateModel(
            name='RssFeed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('rss_id', models.CharField(max_length=200, unique=True)),
                ('published', models.DateTimeField()),
                ('summary', models.TextField()),
                ('tickers', models.ManyToManyField(to='tickers.ticker')),
            ],
        ),
    ]
