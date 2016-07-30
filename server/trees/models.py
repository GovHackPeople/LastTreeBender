from django.contrib.gis.db import models
from django.contrib.gis import measure
import random

class Chair(models.Model):
    
    gisId = models.IntegerField()
    longLat = models.PointField(null=False, blank=False, geography=True)


class TreeType(models.Model):

    commonName = models.CharField(max_length=50)
    scientificName = models.CharField(max_length=50)
    genus = models.CharField(max_length=50)
    family = models.CharField(max_length=50)
    scarcity = models.IntegerField() # TODO: Don't bother storing this, should be able to calculate it at runtime just fine.
    license = models.CharField(max_length=100, null=True)
    artist = models.TextField(max_length=1024, null=True)
    imageUrl = models.TextField(max_length=1024, null=True)
    description = models.TextField(max_length=1024, null=True)


class Tree(models.Model):
    
    comId = models.IntegerField()
    yearPlanted = models.IntegerField(null=True)
    longLat = models.PointField(null=False, blank=False, geography=True)
    treeType = models.ForeignKey(TreeType, on_delete=models.CASCADE)


def random_tree(point):
    trees = Tree.objects.filter(
        longLat__distance_gt=(point, measure.Distance(m=200)),
        longLat__distance_lt=(point, measure.Distance(m=400)))
    
    return random.choice(trees)