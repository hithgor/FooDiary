# Generated by Django 3.0.3 on 2020-03-30 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ruthlesspa', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
