# Generated by Django 2.0.6 on 2018-06-19 00:36

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0016_auto_20180617_1120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='attendance_date',
            field=models.DateField(default=django.utils.timezone.now, max_length=20),
        ),
        migrations.AlterField(
            model_name='guardian',
            name='relation',
            field=models.CharField(choices=[('Father', 'Father'), ('Mother', 'Mother'), ('Brother', 'Brother'), ('Sister', 'Sister'), ('Friend', 'Friend')], max_length=50),
        ),
    ]
