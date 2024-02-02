# Generated by Django 4.2.9 on 2024-02-02 01:20

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='description',
            field=ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='description category'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='body',
            field=ckeditor.fields.RichTextField(verbose_name='comment text'),
        ),
        migrations.AlterField(
            model_name='discount',
            name='description',
            field=ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='description discount'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=ckeditor.fields.RichTextField(blank=True, null=True, verbose_name=' description product'),
        ),
    ]
