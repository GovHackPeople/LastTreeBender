# Developing

## Dependencies

We are using geo-django with a spatialite database backend.

Install the following dependencies via your python package manager of choice (e.g. `pip`):
 *  `django`
 *  `psycopg2`
 *  `requests`

Ensure you follow the [instructions for your OS](https://docs.djangoproject.com/en/1.9/ref/contrib/gis/install/postgis/) to get PostGIS installed.

## Setting up

Setting up a server:
 * `sudo apt-get install postgresql postgis python-pip libpq-dev python3 python3-pip python3-virtualenv uwsgi-plugin-python3 nginx`
 * `create user trees with superuser password 'trees'`;
 * `create database trees;`
 * `pip3 install django psycopg2`

* `virtualenv -p python3 tree-bender`
* `cd tree-bender && source bin/activate`
* `pip install django psycopg2 requests uwsgi encodings`

Follow [these instructions](http://uwsgi-docs.readthedocs.io/en/latest/tutorials/Django_and_nginx.html), they are very detailed and helpful. Things to note are that the .ini file you create should include:
 * `plugin = python`
 * Instead of `module = blah.wsgi` you should use `wsgi-file = server/wsgi.py`

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

# Dependencies

* [Start Bootstrap](http://startbootstrap.com/) - [Grayscale](http://startbootstrap.com/template-overviews/grayscale/) - [Apache2 License](https://www.apache.org/licenses/LICENSE-2.0.html)