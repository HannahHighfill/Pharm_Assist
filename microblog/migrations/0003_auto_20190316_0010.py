# Generated by Django 2.1.7 on 2019-03-16 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('microblog', '0002_auto_20190315_2318'),
    ]

    operations = [
        migrations.AddField(
            model_name='refillevent',
            name='postedtocalendar',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='refillevent',
            name='timezone',
            field=models.CharField(default='America/Los_Angeles', max_length=160),
        ),
    ]