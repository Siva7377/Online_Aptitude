# Generated by Django 4.1 on 2024-02-17 11:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("quiz", "0003_exam_startdate"),
    ]

    operations = [
        migrations.AlterField(
            model_name="exam",
            name="startdate",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 2, 17, 16, 36, 29, 432071)
            ),
        ),
    ]
