# Generated by Django 3.2.5 on 2021-08-07 11:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('service_admin', '0040_auto_20210720_1720'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='announcement',
            options={'managed': False, 'ordering': ['-launch', 'expire'], 'verbose_name': 'Announcement'},
        ),
    ]
