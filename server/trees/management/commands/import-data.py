from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis import geos
from trees.models import Tree, TreeType, Chair
from django.conf import settings
from django.db import transaction
import os
import urllib.request
import csv
import re

class Command(BaseCommand):
    help = 'Import initial datasets'

    def handle(self, *args, **options):
        data = Data(self.stdout)
        data.prepare_raw_data()


class Data:

    def __init__(self, stdout):
        self.stdout = stdout
        self.data_dir = os.path.join(settings.BASE_DIR, "trees", "data")
        self.tree_csv = os.path.join(self.data_dir, "trees.csv")
        self.chair_csv = os.path.join(self.data_dir, "chairs.csv")

    def prepare_raw_data(self):
        """
        Ensure that the required data sets are downloaded and present in the
        data directory, ready for importing into the database.
        """
        if not os.path.isdir(self.data_dir):
            self.stdout.write("Making directory %s" % self.data_dir);
            os.mkdir(self.data_dir);
	
        self.prepare_tree_csv()
        self.parse_tree_csv()
        self.calc_tree_stats();
        
        self.prepare_chair_csv()
        self.parse_chair_csv()

    def prepare_chair_csv(self):
        if not os.path.isfile(self.chair_csv):
            self.stdout.write("Downloading chair.csv file");
            urllib.request.urlretrieve("https://data.melbourne.vic.gov.au/api/views/8fgn-5q6t/rows.csv?accessType=DOWNLOAD", self.chair_csv);
        else:
            self.stdout.write("Using already existing chair.csv file");

    def prepare_tree_csv(self):
        if not os.path.isfile(self.tree_csv):
            self.stdout.write("Downloading tree.csv file");
            urllib.request.urlretrieve("https://data.melbourne.vic.gov.au/api/views/fp38-wiyy/rows.csv?accessType=DOWNLOAD", self.tree_csv);
        else:
            self.stdout.write("Using already existing tree.csv file");
            
    @transaction.atomic
    def parse_chair_csv(self):
        with open(self.chair_csv, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            i = 0;
            for row in reader:
                if row['ASSET_TYPE'] != "Seat":
                    continue
                
                # The "CoordinateLocation comes in a string that looks like:
                #  "(lat, long)"
                # so we capture both of these values and parse into floats.
                regex = re.compile("\((.*), (.*)\)")
                match = regex.match(row['CoordinateLocation'])
                long_lat = geos.Point(float(match.group(2)), float(match.group(1)))
                
                chair = Chair.objects.create(
                    gisId=int(row['GIS_ID']),
                    longLat=long_lat)
                
                i = i + 1
                if i % 500 == 0:
                    self.stdout.write("Inserted %d chairs" % i)

    @transaction.atomic
    def parse_tree_csv(self):
        """
        Each row of the CSV gets parsed into a PHP array that looks like this:

         *   [CoM ID] => 1031823
         *   [Common Name] => White Poplar
         *   [Scientific Name] => Populus alba
         *   [Genus] => Populus
         *   [Family] => Salicaceae
         *   [Diameter Breast Height] => 64
         *   [Year Planted] => 1998
         *   [Date Planted] => 09/02/1998
         *   [Age Description] => Mature
         *   [Useful Life Expectency] => 6-10 years (<50% canopy)
         *   [Useful Life Expectency Value] => 10
         *   [Precinct] => South Yarra & Eastern Parklands
         *   [Located in] => Park
         *   [UploadDate] => 29/07/2016
         *   [CoordinateLocation] => (-37.8320351972647, 144.976732703301)
         *   [Latitude] => -37.8320351972647
         *   [Longitude] => 144.976732703301
         *   [Easting] => 321948.89
         *   [Northing] => 5810892.1

        Right now, we are only storing a subset of this, but we can choose to
        store more if desired/required.
        """

        with open(self.tree_csv, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            i = 0;
            for row in reader:
                treeTypes = TreeType.objects.filter(commonName=row['Common Name'])
                treeType = None
                
                if len(treeTypes) > 0:
                    treeType = treeTypes[0]
                else:
                    treeType = TreeType.objects.create(
                        commonName=row['Common Name'],
                        scientificName=row['Scientific Name'],
                        genus=row['Genus'],
                        family=row['Family'],
                        scarcity=0)
                
                year = None if len(row['Year Planted']) == 0 else int(row['Year Planted'])
                long_lat = geos.Point(float(row['Longitude']), float(row['Latitude']))
                tree = Tree.objects.create(
                    comId=int(row['CoM ID']),
                    yearPlanted=year,
                    treeType=treeType,
                    longLat=long_lat)
                
                i = i + 1
                if i % 500 == 0:
                    self.stdout.write("Inserted %d trees" % i)
                    
    def calc_tree_stats(self):
        for treeType in TreeType.objects.all():
            treeType.scarcity = Tree.objects.filter(treeType=treeType).count()
            treeType.save()