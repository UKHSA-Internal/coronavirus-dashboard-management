# Generated by Django 3.1.7 on 2021-03-04 14:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('service_admin', '0011_auto_20210304_1233'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='yellowbanner',
            name='relative_urls',
        ),
        migrations.DeleteModel(
            name='PageURI',
        ),
        migrations.DeleteModel(
            name='YellowBanner',
        ),
    ]
