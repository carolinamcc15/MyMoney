# Generated by Django 2.2.12 on 2021-10-15 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mymoneyapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='description',
            field=models.CharField(max_length=75),
        ),
    ]