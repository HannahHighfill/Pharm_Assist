# Generated by Django 2.1.7 on 2019-03-20 01:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('microblog', '0005_auto_20190320_0024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='refill',
            name='repeats',
            field=models.CharField(blank=True, choices=[('WEEKLY', 'weeks'), ('MONTHLY', 'months')], max_length=9, null=True),
        ),
        migrations.AlterField(
            model_name='refill',
            name='timezone',
            field=models.CharField(choices=[('-05:00', 'EST'), ('-04:00', 'EDT'), ('-06:00', 'CST'), ('-05:00', 'CDT'), ('-07:00', 'MST'), ('-06:00', 'MDT'), ('-08:00', 'PST'), ('-07:00', 'PDT')], default='PDT', help_text='Timezone of first refill date', max_length=20),
        ),
    ]