# Generated by Django 2.2.15 on 2020-09-02 22:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20200901_0132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetails',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to='profile_image/2020-09-02'),
        ),
    ]