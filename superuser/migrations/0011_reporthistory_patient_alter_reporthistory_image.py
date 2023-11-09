# Generated by Django 4.2.5 on 2023-09-18 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superuser', '0010_alter_reporthistory_cardiologist_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='reporthistory',
            name='patient',
            field=models.CharField(default='Samuel Inkoom', max_length=100),
        ),
        migrations.AlterField(
            model_name='reporthistory',
            name='image',
            field=models.ImageField(default='', null=True, upload_to='cardio-uploads/'),
        ),
    ]