# Generated by Django 3.2.8 on 2021-10-29 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mymoneyapp', '0005_auto_20211016_1627'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
