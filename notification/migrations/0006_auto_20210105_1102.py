# Generated by Django 3.1 on 2021-01-05 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0005_auto_20210104_0908'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='icon',
            field=models.ImageField(blank=True, null=True, upload_to='notification/2021-01-05'),
        ),
    ]
