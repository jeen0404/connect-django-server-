# Generated by Django 3.1 on 2021-01-24 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0008_auto_20210123_0132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='icon',
            field=models.ImageField(blank=True, null=True, upload_to='notification/2021-01-24'),
        ),
    ]
