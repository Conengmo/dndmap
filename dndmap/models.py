import os
import shutil
import subprocess
from PIL import Image

from django.contrib.auth.models import User
from django.contrib.staticfiles import finders
from django.db import models
from django.templatetags.static import static

from .validators import validate_image_extension


class Map(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to="maps/", validators=[validate_image_extension])
    width = models.IntegerField(blank=True)
    height = models.IntegerField(blank=True)

    def __str__(self):
        return f"{self.pk}: {self.name} (user {self.user})"

    @property
    def tiles_urlpath(self):
        return static(f"tiles/{self.pk}/")

    @property
    def tiles_filepath(self):
        result = finders.find("tiles")
        return os.path.join(result, str(self.pk), "")

    def save(self, *args, **kwargs):
        created = not bool(self.pk)
        self._add_dimensions()
        super().save(*args, **kwargs)
        self._refresh_tileset()
        if created:
            for i in range(6):
                Layer.objects.create(name=f'zoom {i}', map=self)

    def _add_dimensions(self):
        img = Image.open(self.file)
        self.width = img.width
        self.height = img.height

    def _refresh_tileset(self):
        shutil.rmtree(self.tiles_filepath, ignore_errors=True)
        # tile generation: fire and forget
        subprocess.Popen(
            f"python bin/gdal2tiles-leaflet.py -l -p raster -z 0-5 -w none {self.file} {self.tiles_filepath}",
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )


class Layer(models.Model):
    map = models.ForeignKey(Map, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.pk}: {self.name} (map {self.map})'

    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'markers': [marker.to_dict() for marker in self.marker_set.all()],
        }


class Marker(models.Model):
    layer = models.ForeignKey(Layer, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f'{self.pk}: {self.name} (layer {self.layer})'

    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'description': self.description,
            'latitude': self.latitude,
            'longitude': self.longitude,
        }
