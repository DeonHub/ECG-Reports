# Generated by Django 4.2.5 on 2023-09-19 00:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('superuser', '0012_rename_total_credits_credit_total_slots_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reporthistory',
            old_name='patient',
            new_name='patient_name',
        ),
        migrations.AddField(
            model_name='reporthistory',
            name='patient_age',
            field=models.IntegerField(default=25, null=True),
        ),
        migrations.AddField(
            model_name='reporthistory',
            name='patient_number',
            field=models.CharField(default='1234567890', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='reporthistory',
            name='patient_type',
            field=models.CharField(default='None', max_length=100),
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('study', models.CharField(max_length=255, null=True)),
                ('clinical_information', models.CharField(max_length=255, null=True)),
                ('report', models.CharField(max_length=255, null=True)),
                ('rhythm', models.CharField(max_length=255, null=True)),
                ('rate', models.CharField(max_length=255, null=True)),
                ('p_wave', models.CharField(max_length=255, null=True)),
                ('st_segment', models.CharField(max_length=255, null=True)),
                ('pr_interval', models.CharField(max_length=255, null=True)),
                ('qrs_complex', models.CharField(max_length=255, null=True)),
                ('t_wave', models.CharField(max_length=255, null=True)),
                ('axis', models.CharField(max_length=255, null=True)),
                ('r_wave_progression', models.CharField(max_length=255, null=True)),
                ('sokolow_lyon_index', models.CharField(max_length=255, null=True)),
                ('r_wave_in_avl', models.CharField(max_length=255, null=True)),
                ('cornel_voltage', models.CharField(max_length=255, null=True)),
                ('qtc', models.CharField(max_length=255, null=True)),
                ('conclusion', models.CharField(max_length=255, null=True)),
                ('recommendation', models.CharField(max_length=255, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('report_history', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='report_history', to='superuser.reporthistory')),
            ],
        ),
    ]
