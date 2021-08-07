# Generated by Django 3.1.7 on 2021-03-04 12:33

from django.db import migrations, models
import markdownx.models
import service_admin.models.fields
import service_admin.models.announcement.banners
from uuid import uuid4


class Migration(migrations.Migration):

    dependencies = [
        ('service_admin', '0010_auto_20210301_1847'),
    ]

    operations = [
        migrations.RunSQL(
            "SET LOCAL citus.multi_shard_modify_mode TO 'sequential';"
        ),
        migrations.CreateModel(
            name='PageURI',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('page_name', service_admin.models.fields.VarCharField(max_length=100)),
                ('display_uri', models.URLField(help_text='Relative URI to the page', verbose_name='URL')),
            ],
            options={
                'verbose_name': 'yellow banner',
                'db_table': 'covid19"."page_uri',
            },
        ),
        migrations.AlterModelOptions(
            name='areareference',
            options={'managed': False, 'verbose_name': 'area'},
        ),
        migrations.AlterModelOptions(
            name='metricreference',
            options={'managed': False, 'verbose_name': 'metric'},
        ),
        migrations.AlterModelOptions(
            name='releasereference',
            options={'managed': False, 'verbose_name': 'release'},
        ),
        migrations.CreateModel(
            name='YellowBanner',
            fields=[
                ('id', service_admin.models.fields.VarCharField(default=uuid4, max_length=36, primary_key=True, serialize=False)),
                ('appear_by_update', models.DateField(verbose_name='appear by update')),
                ('disappear_by_update', models.DateField(verbose_name='disappear by update')),
                ('date', models.DateField(null=True, verbose_name='date')),
                ('body', markdownx.models.MarkdownxField(verbose_name='body')),
                ('relative_urls', models.ManyToManyField(to='service_admin.PageURI')),
            ],
            options={
                'verbose_name': 'yellow banner',
                'db_table': 'covid19"."yellow_banner',
                "manged": False
            },
        ),
        migrations.RunSQL(
            "SELECT create_reference_table('covid19.page_uri')"
        ),
        migrations.RunSQL(
            "SELECT create_reference_table('covid19.yellow_banner_relative_urls')"
        ),
        migrations.RunSQL(
            "SELECT create_reference_table('covid19.yellow_banner')"
        ),
        migrations.RunSQL(
            "SET LOCAL citus.multi_shard_modify_mode TO 'parallel';"
        ),
    ]
