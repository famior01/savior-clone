# Generated by Django 4.1.6 on 2023-02-13 17:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0004_reportiwatch_recorded_reportzakatpost_recorded'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reportiwatch',
            name='Recorded',
        ),
        migrations.RemoveField(
            model_name='reportzakatpost',
            name='Recorded',
        ),
    ]