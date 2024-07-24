# Generated by Django 4.2 on 2024-07-22 23:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='historic_value',
            field=models.DecimalField(blank=True, decimal_places=4, default=0, max_digits=30, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='withdraw_value',
            field=models.DecimalField(blank=True, decimal_places=4, default=0, max_digits=30, null=True),
        ),
    ]
