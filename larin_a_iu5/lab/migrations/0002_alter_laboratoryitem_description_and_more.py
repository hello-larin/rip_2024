# Generated by Django 5.1.1 on 2024-09-25 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lab', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='laboratoryitem',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='laboratoryorder',
            name='address',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='laboratoryorder',
            name='phone',
            field=models.CharField(blank=True, max_length=15),
        ),
    ]