# Generated by Django 2.2.15 on 2020-08-30 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='icon',
            field=models.ImageField(blank=True, null=True, upload_to='notification/2020-08-30'),
        ),
    ]
