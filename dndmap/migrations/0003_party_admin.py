# Generated by Django 3.2.13 on 2022-04-17 19:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dndmap', '0002_auto_20220413_1554'),
    ]

    operations = [
        migrations.AddField(
            model_name='party',
            name='admin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='dndmap.user'),
        ),
    ]
