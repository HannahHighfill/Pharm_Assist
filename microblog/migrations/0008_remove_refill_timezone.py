# Generated by Django 2.1.7 on 2019-03-21 22:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('microblog', '0007_auto_20190320_0154'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='refill',
            name='timezone',
        ),
    ]
