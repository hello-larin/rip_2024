# Generated by Django 5.1.1 on 2024-10-22 07:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LaboratoryItem',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('price', models.IntegerField()),
                ('image', models.TextField(blank=True, null=True)),
                ('status', models.BooleanField(default=1)),
            ],
            options={
                'db_table': 'laboratory_item',
            },
        ),
        migrations.CreateModel(
            name='LaboratoryOrder',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('address', models.TextField(blank=True, null=True)),
                ('phone', models.CharField(blank=True, max_length=15, null=True)),
                ('accepted_date', models.DateTimeField(blank=True, null=True)),
                ('created_date', models.DateTimeField(auto_now=True, null=True)),
                ('status', models.IntegerField()),
                ('submited_date', models.DateTimeField(blank=True, null=True)),
                ('moderator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='m_orders', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='orders', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'laboratory_order',
            },
        ),
        migrations.CreateModel(
            name='LaboratoryOrderItems',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('amount', models.IntegerField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='equipment', to='laboratory.laboratoryorder')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='equipment', to='laboratory.laboratoryitem')),
            ],
            options={
                'db_table': 'laboratory_order_items',
                'unique_together': {('order', 'product_id')},
            },
        ),
    ]
