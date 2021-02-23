# Generated by Django 3.1.5 on 2021-02-23 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gnar_app', '0003_generalpoints_meetingattended_meetinggamewon_miscellaneouspoints_workoutattended'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClimbComplete',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=30)),
                ('climb_id', models.PositiveIntegerField()),
                ('time_added', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
