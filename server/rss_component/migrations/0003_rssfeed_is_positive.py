# Generated by Django 4.2 on 2024-05-14 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rss_component', '0002_rssfeed_is_analysed'),
    ]

    operations = [
        migrations.AddField(
            model_name='rssfeed',
            name='is_positive',
            field=models.BooleanField(default=False),
        ),
    ]
