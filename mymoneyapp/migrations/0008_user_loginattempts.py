# Generated by Django 3.1.4 on 2021-11-04 04:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mymoneyapp', '0007_auto_20211103_2257'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='loginAttempts',
            field=models.IntegerField(default=0),
        ),
    ]
