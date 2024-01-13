# Generated by Django 4.0.4 on 2024-01-13 20:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(default='lab stuff', max_length=20)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='item',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('item', models.CharField(default='thing(s)', max_length=100)),
                ('item_description', models.TextField()),
                ('category', models.ForeignKey(default='lab stuff', on_delete=django.db.models.deletion.SET_DEFAULT, to='inventory.category')),
            ],
        ),
        migrations.CreateModel(
            name='location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(default='lab', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(default='in the void', max_length=10)),
            ],
            options={
                'verbose_name': 'Status',
                'verbose_name_plural': 'Statuses',
            },
        ),
        migrations.CreateModel(
            name='unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit', models.CharField(default='unit(s)', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='vendor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vendor', models.CharField(default='probably some monopoly', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='purchase_reference',
            fields=[
                ('purchase_reference', models.AutoField(primary_key=True, serialize=False)),
                ('catalog', models.CharField(max_length=25)),
                ('price', models.PositiveSmallIntegerField()),
                ('amount', models.PositiveSmallIntegerField()),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.item')),
                ('unit', models.ForeignKey(default='unit(s)', on_delete=django.db.models.deletion.SET_DEFAULT, to='inventory.unit')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.vendor')),
            ],
            options={
                'verbose_name': 'Purchase Reference',
                'verbose_name_plural': 'Purchase References',
            },
        ),
        migrations.CreateModel(
            name='on_request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveSmallIntegerField()),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.item')),
                ('status', models.ForeignKey(default='in the void', on_delete=django.db.models.deletion.SET_DEFAULT, to='inventory.status')),
                ('unit', models.ForeignKey(default='unit(s)', on_delete=django.db.models.deletion.SET_DEFAULT, to='inventory.unit')),
            ],
            options={
                'verbose_name': 'Request',
                'verbose_name_plural': 'Requests',
            },
        ),
        migrations.CreateModel(
            name='inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveSmallIntegerField()),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.item')),
                ('location_name', models.ForeignKey(default='lab', on_delete=django.db.models.deletion.SET_DEFAULT, to='inventory.location')),
                ('unit', models.ForeignKey(default='unit(s)', on_delete=django.db.models.deletion.SET_DEFAULT, to='inventory.unit')),
            ],
            options={
                'verbose_name': 'Inventory',
                'verbose_name_plural': 'Inventory',
            },
        ),
    ]