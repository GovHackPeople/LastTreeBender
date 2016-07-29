from django.contrib.gis.db import models

class Tree(models.Model):
    
    comId = models.IntegerField()
    commonName = models.CharField(max_length=50)
    scientificName = models.CharField(max_length=50)
    genus = models.CharField(max_length=50)
    family = models.CharField(max_length=50)
    yearPlanted = models.IntegerField()
    latLong = models.PointField()