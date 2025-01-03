# Generated by Django 5.0.7 on 2024-12-30 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_remove_userprofile_blocks_remove_userprofile_flats_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='community',
            name='latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='community',
            name='longitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='password',
            field=models.CharField(default='!fst4YrRTsGowywxM3CFZwW91hkJ3UucMJHSo9iwi', max_length=128),
        ),
    ]
