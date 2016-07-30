from django.shortcuts import render
from django.http import HttpResponse
from trees.models import Tree
from django.contrib.gis import geos

def index(request):
    return HttpResponse("Trees!")

def find_trees(request):
    return HttpResponse("Tree")