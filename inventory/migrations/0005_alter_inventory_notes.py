# Generated by Django 4.0.4 on 2024-02-03 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0004_inventory_notes_location_lab_alter_inventory_amount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='notes',
            field=models.TextField(default=None, null=True),
        ),
    ]
