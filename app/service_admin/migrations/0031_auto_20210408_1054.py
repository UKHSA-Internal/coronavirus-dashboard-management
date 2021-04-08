# Generated by Django 3.1.7 on 2021-04-08 10:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('service_admin', '0030_auto_20210317_0957'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='announcement',
            options={'managed': False, 'verbose_name': 'Announcement'},
        ),
        migrations.AlterModelOptions(
            name='bannerpage',
            options={'managed': False, 'verbose_name': 'banner page'},
        ),
        migrations.AlterModelOptions(
            name='metricasset',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='metricassettometric',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='metrictag',
            options={'managed': False, 'ordering': ('metric', '-tag')},
        ),
        migrations.AlterModelOptions(
            name='releasereference',
            options={'managed': False, 'ordering': ('-timestamp',), 'verbose_name': 'release'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'managed': False, 'verbose_name': 'Tag', 'verbose_name_plural': 'Tags'},
        ),
    ]