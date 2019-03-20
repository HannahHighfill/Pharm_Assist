# Generated by Django 2.1.7 on 2019-03-20 00:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('microblog', '0003_auto_20190319_2330'),
    ]

    operations = [
        migrations.AddField(
            model_name='refill',
            name='timezone',
            field=models.CharField(blank=True, choices=[('-5:00', 'EST'), ('-4:00', 'EDT'), ('-6:00', 'CST'), ('-5:00', 'CDT'), ('-7:00', 'MST'), ('-6:00', 'MDT'), ('-8:00', 'PST'), ('-7:00', 'PDT')], help_text='Timezone of first refill date', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='refill',
            name='all_day',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AlterField(
            model_name='refill',
            name='repeats',
            field=models.CharField(blank=True, choices=[('weeks', 'weeks'), ('months', 'months')], help_text='every', max_length=9, null=True),
        ),
    ]
