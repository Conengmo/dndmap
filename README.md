# dndmap

Django webapp that lets you:
- turn an image of a map into an interactive map
- let you and your friends add markers to the map

I use this to share maps from my D&D game with my party and let them add locations they visited. This webapp could be useful for any TTRPG, or any map really.

<img width="990" alt="image" src="https://user-images.githubusercontent.com/33519926/163684956-b68fd9b6-7fa2-4457-88dd-66e3f478c8ad.png">


## Development resources
We use this library to convert an image into a Leaflet tileset:
https://github.com/commenthol/gdal2tiles-leaflet

It's included in this repo, use it like this:
```
python bin/gdal2tiles-leaflet.py -l -p raster -z 0-5 -w none <image> <output folder>
```

And used some code from here for Leaflet settings:
https://github.com/commenthol/leaflet-rastercoords

### Installing gdal
This is a bit more involved than your average Python library. I found this guide useful:
https://mothergeo-py.readthedocs.io/en/latest/development/how-to/gdal-ubuntu-pkg.html

I installed the Python bindings with ```pip install pygdal=="`gdal-config --version`.*"```


## Deployment

I'm using a server with Nginx and uWSGI.

### Nginx
For Nginx you may have to increase the allowed upload file size, since some of these maps can be quite large:

`client_max_body_size 20M;`

### Systemd example
I use Systemd to manage my services. Example systemd service file to start uwsgi:

```
[Service]
User=<username>
Group=www-data
Environment="DJANGO_SECRET_KEY=<secret key>"
Environment="DJANGO_SETTINGS_MODULE=dndmap.settings.prod"
WorkingDirectory=/home/<username>/dndmap/
ExecStart=/home/<username>/venvs/dndmap/bin/uwsgi --ini dndmap.ini

[Install]
WantedBy=multi-user.target
```

### Deployment script
For convenience I made a script to run on the remote server whenever an update is needed:

```bash
#!/bin/bash
cd ~/dndmap/
export DJANGO_SETTINGS_MODULE=dndmap.settings.prod
export "DJANGO_SECRET_KEY=<secret key>"
~/venvs/dndmap/bin/python manage.py collectstatic --ignore tiles/ --noinput
~/venvs/dndmap/bin/python manage.py migrate
sudo systemctl restart dndmap
```
