# Developing

## Dependencies

We are using geo-django with a spatialite database backend.

Install the following dependencies via your python package manager of choice (e.g. `pip`):
 *  `django`
 *  `psycopg2`

Ensure you follow the [instructions for your OS](https://docs.djangoproject.com/en/1.9/ref/contrib/gis/install/postgis/) to get PostGIS installed.

## Setting up

All these commands are to be run from the `server/` directory.

* Create the database: `python manage.py migrate`
* Create admin user: `python manage.py createsuperuser`
* Import data: `python manage.py import-data`
 + Download a .csv of tree data (if not already present)
 + Insert tree data into the database

# Data Sources

## Tree Data

Source: https://data.melbourne.vic.gov.au/Environment/Melbourne-s-Urban-Forest-Tree-data/fp38-wiyy
Source: http://melbourneurbanforestvisual.com.au/
License: http://creativecommons.org/licenses/by/3.0/au/deed.en

## Outdoor furniture

Source: https://data.melbourne.vic.gov.au/Assets-Infrastructure/Outdoor-Furniture/8fgn-5q6t
License: http://creativecommons.org/licenses/by/3.0/au/deed.en
