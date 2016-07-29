# Developing

## Dependencies

We are using geo-django with a spatialite database backend.

Install the following dependencies via your python package manager of choice (e.g. `pip`):
 *  `django`

Ensure you follow the [instructions for your OS](https://docs.djangoproject.com/en/1.9/ref/contrib/gis/install/spatialite/) to get libspatialite installed.

## Setting up database

From the `server/` directory, run `python manage.py migrate`

## Importing Data

From the `server/` directory, run `python manage.py import-data`. This will:
 * Download a .csv of tree data (if not already present)
 * Insert tree data into the database

# Data Sources

## Tree Data

Source: https://data.melbourne.vic.gov.au/Environment/Melbourne-s-Urban-Forest-Tree-data/fp38-wiyy
Source: http://melbourneurbanforestvisual.com.au/
License: http://creativecommons.org/licenses/by/3.0/au/deed.en

## Outdoor furniture

Source: https://data.melbourne.vic.gov.au/Assets-Infrastructure/Outdoor-Furniture/8fgn-5q6t
License: http://creativecommons.org/licenses/by/3.0/au/deed.en
