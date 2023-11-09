# Generated by Django 4.2.5 on 2023-09-18 03:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superuser', '0011_reporthistory_patient_alter_reporthistory_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='credit',
            old_name='total_credits',
            new_name='total_slots',
        ),
        migrations.RemoveField(
            model_name='credit',
            name='hospital',
        ),
        migrations.AddField(
            model_name='credit',
            name='total_amount',
            field=models.FloatField(default=0.0),
        ),
    ]
