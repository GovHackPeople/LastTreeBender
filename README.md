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
 * `sudo apt-get install postgresql postgis python-pip libpq-dev python3 python3-pip apache2 libapache2-mod-wsgi-py3`
 * `create user trees with superuser password 'trees'`;
 * `create database trees;`
 * `pip3 install django psycopg2`

All these commands are to be run from the `server/` directory.

* Create the database: `python manage.py migrate`
* Create admin user: `python manage.py createsuperuser`
* Import data: `python manage.py import-data`
 + Download a .csv of tree data (if not already present)
 + Insert tree data into the database

Configuring Apache2 + mod_wsgi:
* `a2enmod wsgi`

```
WSGIScriptAlias / /path/to/mysite.com/mysite/wsgi.py
WSGIPythonPath /path/to/mysite.com

<Directory /path/to/LastTreeBender/server/server/wsgi.py>
        <Files wsgi.py>
                Require all granted
        </Files>
</Directory>
```


# Data Sources

## Tree Data

Source: https://data.melbourne.vic.gov.au/Environment/Melbourne-s-Urban-Forest-Tree-data/fp38-wiyy
Source: http://melbourneurbanforestvisual.com.au/
License: http://creativecommons.org/licenses/by/3.0/au/deed.en

## Outdoor furniture

Source: https://data.melbourne.vic.gov.au/Assets-Infrastructure/Outdoor-Furniture/8fgn-5q6t
License: http://creativecommons.org/licenses/by/3.0/au/deed.en
