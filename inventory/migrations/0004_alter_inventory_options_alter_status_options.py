# Generated by Django 4.0.4 on 2024-01-13 21:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_alter_item_id'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='inventory',
            options={},
        ),
        migrations.AlterModelOptions(
            name='status',
            options={'verbose_name': 'Status', 'verbose_name_plural': 'Status'},
        ),
    ]