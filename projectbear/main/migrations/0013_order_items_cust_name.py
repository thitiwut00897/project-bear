# Generated by Django 3.0.2 on 2020-04-15 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_auto_20200415_1526'),
    ]

    operations = [
        migrations.AddField(
            model_name='order_items',
            name='cust_name',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
