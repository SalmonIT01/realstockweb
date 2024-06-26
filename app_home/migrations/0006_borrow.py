# Generated by Django 4.2.2 on 2023-11-14 03:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_home', '0005_alter_details_product_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Borrow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('b_amount', models.FloatField(default='', max_length=20)),
                ('borrow_date', models.DateField()),
                ('return_date', models.DateField(null=True)),
                ('b_productid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_home.details')),
            ],
        ),
    ]
