# Generated by Django 3.2.4 on 2021-06-03 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_rename_is_stuff_account_is_staff'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='profile_image',
            field=models.ImageField(blank=True, default='default_profile_image.png', max_length=255, null=True, upload_to='profile/'),
        ),
    ]
