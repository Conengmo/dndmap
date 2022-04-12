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
