# Generated by Django 5.0.7 on 2024-09-30 06:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_alter_userprofile_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='community',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.community'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='password',
            field=models.CharField(default='!hDZXOtEvuGBMtrBKY29fiRAUZDJO3bqT8lUhMlrl', max_length=128),
        ),
    ]
