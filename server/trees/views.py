from django.shortcuts import render
from django.http import HttpResponse
from trees.models import Tree
from django.contrib.gis import geos
from django.contrib.gis import measure

def index(request):
    return HttpResponse("Trees!")

def view_map(request):
    thoughtworks = geos.GEOSGeometry('POINT(%s %s)' % (-37.816399, 144.964004))
    trees = Tree.objects.filter(
        latLong__distance_gt=(thoughtworks, measure.Distance(Metre=200)),
        latLong__distance_lt=(thoughtworks, measure.Distance(Metre=400)))
    return HttpResponse("%d trees" % len(trees))