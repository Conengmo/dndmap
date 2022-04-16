# dndmap

## Resources
https://github.com/commenthol/gdal2tiles-leaflet
https://github.com/commenthol/leaflet-rastercoords

Installing gdal
https://mothergeo-py.readthedocs.io/en/latest/development/how-to/gdal-ubuntu-pkg.html
Ended up installing `pip install pygdal=="`gdal-config --version`.*"`
 
## Generating tileset
```
python bin/gdal2tiles-leaflet.py -l -p raster -z 0-5 -w none <image> <output folder>
```

# Deployment

I'm using a server with Nginx and uWSGI.

For Nginx you may have to increase the allowed upload file size, since some of these maps can be quite large:

`client_max_body_size 20M;`

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
