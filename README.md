# Developing

## Configuring PHP

We are using sqlite with the spatialite extension in order to do spatial queries.
Apologies for this choice, because PHP + spatialite is a pain to configure, which was not known before chosing to use it.

To configure PHP using spatialite:
 * [Install the php-sqlite module](http://php.net/manual/en/sqlite3.installation.php) (seems to be preconfigured in most PHP installs).
 * Download [libspatialite](http://www.gaia-gis.it/gaia-sins/)
  + On Windows, [there are binaries for download at the bottom of this page](http://www.gaia-gis.it/gaia-sins/)
  + On Linux, most distributions probably package `libspatialite`
 * [Configure your `php.ini` `sqlite3.extension_dir`](http://www.gaia-gis.it/spatialite-2.4.0-4/splite-php.html)
 * Ensure that the downloaded `mod_spatialite.so` (Linux) or `mod_spatialite.dll` (Windows) is available in your `sqlite3.extension_dir`.

# Data Sources

## Tree Data

Source: https://data.melbourne.vic.gov.au/Environment/Melbourne-s-Urban-Forest-Tree-data/fp38-wiyy
Source: http://melbourneurbanforestvisual.com.au/
License: http://creativecommons.org/licenses/by/3.0/au/deed.en


## Outdoor furniture

Source: https://data.melbourne.vic.gov.au/Assets-Infrastructure/Outdoor-Furniture/8fgn-5q6t
License: http://creativecommons.org/licenses/by/3.0/au/deed.en
