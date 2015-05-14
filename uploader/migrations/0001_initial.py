# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.files.storage


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Upload',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uploaded_file', models.FileField(storage=django.core.files.storage.FileSystemStorage(), upload_to=b'uploads')),
                ('date_uploaded', models.DateTimeField(auto_now_add=True)),
                ('admin_url', models.CharField(default=b'', max_length=255, blank=True)),
                ('object_id', models.PositiveIntegerField(null=True, blank=True)),
                ('thumbnail_attr', models.CharField(default=b'', max_length=255, null=True, blank=True)),
                ('content_type', models.ForeignKey(blank=True, to='contenttypes.ContentType', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
