# Generated by Django 4.2.3 on 2023-12-07 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("todoappv2", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="todolist",
            name="done_status",
            field=models.BooleanField(default=False),
        ),
    ]
