# Generated by Django 5.0.6 on 2024-08-03 08:55

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_metatag'),
    ]

    operations = [
        migrations.AddField(
            model_name='metatag',
            name='og_description',
            field=models.TextField(default=django.utils.timezone.now, help_text='Enter the open graph description for the page.'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='metatag',
            name='og_title',
            field=models.CharField(default=django.utils.timezone.now, help_text='Enter the open graph title for the page.', max_length=200),
            preserve_default=False,
        ),
    ]
