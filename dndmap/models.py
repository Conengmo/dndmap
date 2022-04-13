import math
import os
import shutil
import subprocess
from PIL import Image

from django.contrib.auth.models import AbstractUser
from django.contrib.staticfiles import finders
from django.db import models
from django.templatetags.static import static

from . import settings
from .validators import validate_image_extension


class Party(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.id}: {self.name}"


class User(AbstractUser):
    party = models.ForeignKey(Party, on_delete=models.CASCADE, blank=True, null=True)


class Map(models.Model):
    name = models.CharField(max_length=255)
    party = models.ForeignKey(Party, on_delete=models.CASCADE)
    file = models.FileField(upload_to="maps/", validators=[validate_image_extension])
    width = models.IntegerField(blank=True)
    height = models.IntegerField(blank=True)
    min_zoom = models.IntegerField(default=1)
    max_zoom = models.IntegerField(default=5)

    _original_file = None
    _original_zoom = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._original_file = self.file
        self._original_zoom = (self.min_zoom, self.max_zoom)

    def __str__(self):
        return f"{self.pk}: {self.name} (party {self.party})"

    @property
    def tiles_urlpath(self):
        return static(f"tiles/{self.pk}/")

    @property
    def tiles_filepath(self):
        result = finders.find("tiles")
        return os.path.join(result, str(self.pk), "")

    def save(self, *args, **kwargs):
        created = not bool(self.pk)
        is_file_changed = self._original_file != self.file
        if is_file_changed:
            self._add_dimensions()
        if created:
            self._set_max_zoom()
        super().save(*args, **kwargs)
        if is_file_changed or self._original_zoom != (self.min_zoom, self.max_zoom):
            self._refresh_tileset()
        if created:
            Layer.objects.create(name='default', map=self)

    def _add_dimensions(self):
        img = Image.open(self.file)
        self.width = img.width
        self.height = img.height

    def _set_max_zoom(self):
        """Calculate a maximum zoom level that fits given the image size."""
        tilesize = 256
        self.max_zoom = math.ceil(
            math.log(
                max(self.width, self.height) / tilesize
            ) / math.log(2)
        )

    def _refresh_tileset(self):
        shutil.rmtree(self.tiles_filepath, ignore_errors=True)
        # tile generation: fire and forget
        subprocess.Popen(
            f"{settings.PYTHON_EXECUTABLE} bin/gdal2tiles-leaflet.py"
            f" -l -p raster -z {self.min_zoom}-{self.max_zoom} -w none"
            f" {self.file} {self.tiles_filepath}",
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )


class Layer(models.Model):
    map = models.ForeignKey(Map, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    show_at_zoom_level = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.id}: {self.name} (map {self.map})'

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'show_at_zoom_level': self.show_at_zoom_level,
            'markers': [marker.to_dict() for marker in self.marker_set.all()],
        }


class Marker(models.Model):

    class ColorOptions(models.TextChoices):
        RED = 'red'
        DARKRED = 'darkred'
        ORANGE = 'orange'
        GREEN = 'green'
        DARKGREEN = 'darkgreen'
        BLUE = 'blue'
        PURPLE = 'purple'
        DARKPURPLE = 'darkpurple'
        CADETBLUE = 'cadetblue'

    layer = models.ForeignKey(Layer, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    color = models.CharField(max_length=16, choices=ColorOptions.choices)
    icon = models.CharField(max_length=255)
    icon_color = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.id}: {self.name} (layer {self.layer})'

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'layer_id': self.layer_id,
            'color': self.color,
            'icon': self.icon,
            'icon_color': self.icon_color,
        }


