# Generated by Django 3.1.7 on 2021-03-01 14:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('service_admin', '0008_auto_20210301_1447'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='service',
            options={'ordering': ('pk',), 'permissions': (('manage_service_object', 'Can manage service'), ('view_service_object', 'Can view service'), ('create_metric_object', 'Can manage metrics'), ('manage_metric_object', 'Can manage metrics'), ('view_metric_object', 'Can manage metrics'), ('manage_release_object', 'Can despatch data'), ('view_release_object', 'Can view despatch'), ('create_banner_object', 'Can manage banners'), ('manage_banner_object', 'Can manage banners'), ('view_banner_object', 'Can view banners'), ('create_changelog_object', 'Can create change logs'), ('manage_changelog_object', 'Can manage change logs'), ('view_changelog_object', 'Can view change logs'), ('create_metricdoc_object', 'Can create metric documentations'), ('manage_metricdoc_object', 'Can manage metric documentations'), ('view_metricdoc_object', 'Can view metric documentations')), 'verbose_name': 'service', 'verbose_name_plural': 'services'},
        ),
    ]
