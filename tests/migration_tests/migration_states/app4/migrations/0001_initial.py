# Generated by Django 2.2.8 on 2020-02-06 12:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='A1',
            fields=[
                ('id', models.AutoField(help_text='Primary key for Base class.', primary_key=True, serialize=False)),
                ('last_modified', models.DateTimeField(auto_now=True, help_text='Date the class was last modified')),
                ('tag', models.CharField(blank=True, help_text='User defined tag for easy searches', max_length=200, null=True)),
                ('i', models.IntegerField()),
                ('user', models.ForeignKey(blank=True, help_text='User who updated this object. Set on save by connection to database. Ananymous if not found.', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
