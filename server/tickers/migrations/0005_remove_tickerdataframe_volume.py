# Generated by Django 4.2 on 2024-01-06 14:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickers', '0004_alter_tickerdataframe_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tickerdataframe',
            name='volume',
        ),
    ]
