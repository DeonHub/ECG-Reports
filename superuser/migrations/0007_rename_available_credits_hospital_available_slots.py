# Generated by Django 4.2.5 on 2023-09-17 15:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superuser', '0006_alter_cardiologist_profile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hospital',
            old_name='available_credits',
            new_name='available_slots',
        ),
    ]
