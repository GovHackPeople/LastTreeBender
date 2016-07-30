from django.contrib.gis.db import models
from django.contrib.gis import measure
import random

class Chair(models.Model):
    
    gisId = models.IntegerField()
    longLat = models.PointField(null=False, blank=False, geography=True)


class Tree(models.Model):
    
    comId = models.IntegerField()
    commonName = models.CharField(max_length=50)
    scientificName = models.CharField(max_length=50)
    genus = models.CharField(max_length=50)
    family = models.CharField(max_length=50)
    yearPlanted = models.IntegerField()
    longLat = models.PointField(null=False, blank=False, geography=True)

def random_tree(point):
    trees = Tree.objects.filter(
        longLat__distance_gt=(point, measure.Distance(m=200)),
        longLat__distance_lt=(point, measure.Distance(m=400)))
    
    return random.choice(trees)