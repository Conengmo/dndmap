# Generated by Django 3.2.12 on 2022-04-10 13:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import dndmap.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Map',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('file', models.FileField(upload_to='maps/', validators=[dndmap.validators.validate_image_file_extension])),
                ('width', models.IntegerField(blank=True)),
                ('height', models.IntegerField(blank=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
