# Generated by Django 2.2.8 on 2020-02-06 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app3", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="a1", name="j", field=models.IntegerField(default=1),
        ),
    ]
