# Generated by Django 3.0.5 on 2021-06-17 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0002_remove_student_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='audio',
            field=models.FileField(blank=True, default='C:/Users/Master/Desktop/Speaker Identification/AudioTest.wav', null=True, upload_to='audio/Student/'),
        ),
    ]
