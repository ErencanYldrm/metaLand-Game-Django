# Generated by Django 4.1.7 on 2023-05-19 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mlGame', '0006_rename_alanno_alan_alannox_alan_alannoy'),
    ]

    operations = [
        migrations.AddField(
            model_name='oyun',
            name='günSayısı',
            field=models.IntegerField(default=0),
        ),
    ]
