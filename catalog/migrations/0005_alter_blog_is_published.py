# Generated by Django 4.2.3 on 2023-07-29 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_blog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='is_published',
            field=models.BooleanField(verbose_name='Признак публикации'),
        ),
    ]