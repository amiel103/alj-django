# Generated by Django 5.0.3 on 2024-04-08 06:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sales',
            name='code',
        ),
        migrations.RemoveField(
            model_name='sales',
            name='sub_total',
        ),
        migrations.RemoveField(
            model_name='sales',
            name='tax',
        ),
        migrations.RemoveField(
            model_name='sales',
            name='tax_amount',
        ),
    ]
