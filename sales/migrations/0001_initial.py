# Generated by Django 3.2.6 on 2021-10-22 09:38

from django.db import migrations, models
import django.db.models.deletion
import sales.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('code', models.CharField(max_length=6, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('include_in_channel_planning', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='CustomerPlanType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='PlanItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='PlanType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('FORECAST', 'Forecast'), ('BUDGET', 'Budget')], max_length=50, unique=True)),
                ('year', models.IntegerField(choices=[(2021, 2021), (2022, 2022), (2023, 2023), (2024, 2024), (2025, 2025), (2026, 2026), (2027, 2027), (2028, 2028), (2029, 2029), (2030, 2030)], default=sales.models.PlanType.current_year)),
            ],
        ),
        migrations.CreateModel(
            name='SalesChannel',
            fields=[
                ('code', models.CharField(max_length=5, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='UploadData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.FileField(upload_to='tmp_data')),
                ('uploaded', models.DateTimeField(auto_now=True)),
                ('activated', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='SalesRecords',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('quantity', models.FloatField()),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.customer')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
            ],
            options={
                'verbose_name_plural': 'Sales Records',
            },
        ),
        migrations.CreateModel(
            name='SalesPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('period', models.DateField(blank=True, null=True)),
                ('cpt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.customerplantype')),
            ],
        ),
        migrations.AddConstraint(
            model_name='saleschannel',
            constraint=models.UniqueConstraint(fields=('code', 'name'), name='sales_saleschannel_is_unique'),
        ),
        migrations.AddField(
            model_name='planitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product'),
        ),
        migrations.AddField(
            model_name='planitem',
            name='sales_plan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.salesplan'),
        ),
        migrations.AddField(
            model_name='customerplantype',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.customer'),
        ),
        migrations.AddField(
            model_name='customerplantype',
            name='plan_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.plantype'),
        ),
        migrations.AddField(
            model_name='customer',
            name='portfolio',
            field=models.ManyToManyField(blank=True, to='products.Product'),
        ),
        migrations.AddField(
            model_name='customer',
            name='sales_channel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.saleschannel'),
        ),
        migrations.AddConstraint(
            model_name='salesplan',
            constraint=models.UniqueConstraint(fields=('period', 'cpt'), name='sales_salesplan_is_unique'),
        ),
        migrations.AddConstraint(
            model_name='planitem',
            constraint=models.UniqueConstraint(fields=('sales_plan', 'product'), name='sales_planitem_is_unique'),
        ),
        migrations.AddConstraint(
            model_name='customerplantype',
            constraint=models.UniqueConstraint(fields=('customer', 'plan_type'), name='sales_customerplantype_is_unique'),
        ),
        migrations.AddConstraint(
            model_name='customer',
            constraint=models.UniqueConstraint(fields=('code', 'name'), name='sales_customer_is_unique'),
        ),
    ]