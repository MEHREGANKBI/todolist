# Generated by Django 5.0 on 2024-01-10 23:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tokenblocklist',
            old_name='token',
            new_name='refresh_token',
        ),
    ]