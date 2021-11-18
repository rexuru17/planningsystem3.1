# Generated by Django 3.2.9 on 2021-11-17 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0003_auto_20211117_0814'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='customerportfolio',
            constraint=models.UniqueConstraint(fields=('customer', 'product'), name='sales_customerportfolio_is_unique'),
        ),
    ]
