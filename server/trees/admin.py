from django.contrib.gis import admin
from trees.models import Tree

admin.site.register(Tree, admin.GeoModelAdmin)