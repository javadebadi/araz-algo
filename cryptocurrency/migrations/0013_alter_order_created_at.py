# Generated by Django 3.2.7 on 2021-09-11 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cryptocurrency', '0012_rename_cancel_exists_order_cancel_exist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='created_at',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
