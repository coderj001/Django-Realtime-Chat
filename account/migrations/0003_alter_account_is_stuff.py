# Generated by Django 3.2.4 on 2021-06-03 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20210603_0517'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='is_stuff',
            field=models.BooleanField(default=False, verbose_name='Stuff Status'),
        ),
    ]
