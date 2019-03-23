# Generated by Django 2.1.7 on 2019-03-20 00:24

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('microblog', '0004_auto_20190320_0011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='refill',
            name='often',
            field=models.IntegerField(blank=True, default=1, help_text='every', null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(20)]),
        ),
        migrations.AlterField(
            model_name='refill',
            name='repeats',
            field=models.CharField(blank=True, choices=[('weeks', 'weeks'), ('months', 'months')], max_length=9, null=True),
        ),
        migrations.AlterField(
            model_name='refill',
            name='timezone',
            field=models.CharField(blank=True, choices=[('-05:00', 'EST'), ('-04:00', 'EDT'), ('-06:00', 'CST'), ('-05:00', 'CDT'), ('-07:00', 'MST'), ('-06:00', 'MDT'), ('-08:00', 'PST'), ('-07:00', 'PDT')], default='-7:00', help_text='Timezone of first refill date', max_length=20),
        ),
    ]