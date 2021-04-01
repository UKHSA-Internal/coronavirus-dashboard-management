# Generated by Django 3.1.7 on 2021-03-04 15:26

from django.db import migrations, models
import markdownx.models
import service_admin.models.fields
import service_admin.models.shared_models.page_uris
import service_admin.utils.default_generators


class Migration(migrations.Migration):

    dependencies = [
        ('service_admin', '0012_auto_20210304_1456'),
    ]

    operations = [
        migrations.RunSQL(
            "SET LOCAL citus.multi_shard_modify_mode TO 'sequential';"
        ),
        migrations.CreateModel(
            name='PageURI',
            fields=[
                ('id', service_admin.models.fields.VarCharField(default=service_admin.utils.default_generators.generate_unique_id, max_length=36, primary_key=True, serialize=False, verbose_name='unique ID')),
                ('page_name', service_admin.models.fields.VarCharField(max_length=100)),
                ('display_uri', service_admin.models.fields.VarCharField(max_length=150, validators=[service_admin.models.shared_models.page_uris.url_validator])),
            ],
            options={
                'verbose_name': 'Page URI',
                'db_table': 'covid19"."page_uri',
            },
        ),
        migrations.CreateModel(
            name='YellowBanner',
            fields=[
                ('id', service_admin.models.fields.VarCharField(default=service_admin.utils.default_generators.generate_unique_id, max_length=36, primary_key=True, serialize=False, verbose_name='unique ID')),
                ('appear_by_update', models.DateField(verbose_name='appear by update')),
                ('disappear_by_update', models.DateField(verbose_name='disappear by update')),
                ('date', models.DateField(null=True, verbose_name='date')),
                ('body', markdownx.models.MarkdownxField(verbose_name='body')),
                ('relative_urls', models.ManyToManyField(to='service_admin.PageURI')),
            ],
            options={
                'verbose_name': 'yellow banner',
                'db_table': 'covid19"."yellow_banner',
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
