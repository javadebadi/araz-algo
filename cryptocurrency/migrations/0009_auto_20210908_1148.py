# Generated by Django 3.2.7 on 2021-09-08 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cryptocurrency', '0008_candlestick'),
    ]

    operations = [
        migrations.AddField(
            model_name='candlestick',
            name='min_o1',
            field=models.BooleanField(default=1.0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='candlestick',
            name='min_o2',
            field=models.BooleanField(default=1.0),
            preserve_default=False,
        ),
    ]