# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-09-22 11:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_article_article_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='article_title',
            field=models.CharField(max_length=50, unique=True, verbose_name='Назва статті'),
        ),
    ]