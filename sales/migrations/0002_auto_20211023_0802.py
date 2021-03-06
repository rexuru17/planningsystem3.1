# Generated by Django 3.2.8 on 2021-10-23 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plantype',
            name='name',
            field=models.CharField(choices=[('FORECAST', 'Forecast'), ('BUDGET', 'Budget')], max_length=50, verbose_name='Plan Type'),
        ),
        migrations.AddConstraint(
            model_name='plantype',
            constraint=models.UniqueConstraint(fields=('name', 'year'), name='sales_plantype_is_unique'),
        ),
    ]
