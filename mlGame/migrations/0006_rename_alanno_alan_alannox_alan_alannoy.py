# Generated by Django 4.1.7 on 2023-05-18 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mlGame', '0005_alter_alan_alantürü'),
    ]

    operations = [
        migrations.RenameField(
            model_name='alan',
            old_name='alanNo',
            new_name='alanNoX',
        ),
        migrations.AddField(
            model_name='alan',
            name='alanNoY',
            field=models.IntegerField(default=0),
        ),
    ]