# Generated by Django 2.2.15 on 2020-09-07 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0007_auto_20200906_0030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='icon',
            field=models.ImageField(blank=True, null=True, upload_to='notification/2020-09-07'),
        ),
    ]