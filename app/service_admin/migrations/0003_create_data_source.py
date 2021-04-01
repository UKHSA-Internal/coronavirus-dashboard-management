# Generated by Django 3.1.7 on 2021-03-01 13:07

from django.db import migrations, models
import django.db.models.deletion
import service_admin.models


class Migration(migrations.Migration):

    dependencies = [
        ('service_admin', '0002_create_abstract'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataSource',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('label', service_admin.models.VarCharField(max_length=255)),
                ('source', models.TextField()),
                ('applicable_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sources',
                                                    limit_choices_to={'area_type__in': ['overview', 'nation']},
                                                    to='service_admin.areareference')),
            ],
            options={
                'db_table': 'covid19\".\"data_source',
            },
        ),
        migrations.RunSQL(
            "SELECT create_reference_table('covid19.data_source')"
        ),
    ]
