# Generated by Django 3.0.2 on 2020-04-11 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='picture',
            field=models.ImageField(blank=True, default='default_pic.png', null=True, upload_to='user'),
        ),
    ]