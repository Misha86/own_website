# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('category_title', models.CharField(max_length=50, verbose_name='Назва категорії')),
                ('category_name', models.SlugField(verbose_name='Ім`я категорії транслітом')),
                ('category_number', models.IntegerField(default=1, verbose_name='Номер категорії')),
                ('category_url', models.CharField(max_length=200, verbose_name='Адреса для виконання', blank=True)),
            ],
            options={
                'verbose_name_plural': 'Категорії',
                'ordering': ['category_number'],
                'verbose_name': 'Категорія',
                'db_table': 'categories',
            },
        ),
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('menu_title', models.CharField(max_length=50, verbose_name='Назва пункту меню')),
                ('menu_name', models.SlugField(verbose_name='Ім`я пункту меню транслітом')),
                ('menu_number', models.IntegerField(default=1, verbose_name='Номер пункту меню')),
                ('menu_url', models.CharField(max_length=200, verbose_name='Адреса для виконання', blank=True)),
                ('menu_type', models.CharField(max_length=50, verbose_name='Тип пункту меню', choices=[('single', 'звичайний'), ('single active', 'звичайний активний'), ('dropdown', 'випадаючий')])),
            ],
            options={
                'verbose_name_plural': 'Пункти меню',
                'verbose_name': 'Пункт меню',
                'db_table': 'menu_items',
            },
        ),
        migrations.AddField(
            model_name='category',
            name='menu_category',
            field=models.ForeignKey(related_name='categories', to='navigation.MenuItem', verbose_name='пункт меню'),
        ),
    ]
