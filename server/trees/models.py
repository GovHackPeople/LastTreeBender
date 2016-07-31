from django.contrib.gis.db import models
from django.contrib.gis import measure
from django.db.models import Max
import math
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
        longLat__distance_lt=(point, measure.Distance(m=400))
    ).exclude(
        treeType__imageUrl=None,
    ).exclude(
        # For now, exclude these. Will need to figure out why these got here at some point.
        treeType__imageUrl='https://upload.wikimedia.org/wikipedia/en/4/4a/Commons-logo.svg'
    )
    
    return roulette_wheel_random_choice(trees)

def roulette_wheel_random_choice(trees):
    """
    Select from the choice of trees, but weight the choice so it is more likely
    to choose a scarce tree than a common tree.
    Inspired by http://stackoverflow.com/a/10324090
    """
    
    def log_scarcity(tree):
        tree.__log_scarcity__ = int(math.log(tree.treeType.scarcity))
        return tree
    
    trees_log_scarcity = list(map(log_scarcity, trees))
    log_scarcity_values = [t.__log_scarcity__ for t in trees_log_scarcity]
    max_log_scarcity = max(log_scarcity_values)
    total_scarcity = sum(log_scarcity_values)
    pick = random.uniform(0, total_scarcity)
    
    current = 0
    for tree in list(trees_log_scarcity):
        to_add = max_log_scarcity - tree.__log_scarcity__
        current += to_add
        if current > pick:
            return tree
    
    return trees_log_scarcity.pop()