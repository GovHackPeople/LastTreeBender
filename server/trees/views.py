from django.http import HttpResponse, JsonResponse
from django.template import loader
from trees.models import random_tree
from django.contrib.gis import geos

def index(request):
    template = loader.get_template('trees/index.html')
    return HttpResponse(template.render({}, request))

def view_map(request):
    thoughtworks = geos.Point(144.964004, -37.816399)
    tree = random_tree(thoughtworks)
    
    return JsonResponse({
        'metadata' : {
            'title': tree.treeType.commonName,
            'description': 'Also known as "%s"' % tree.treeType.scientificName
        },
        'source': {
            'lat': thoughtworks.y,
            'lon': thoughtworks.x
        },
        'dest': {
            'lat': tree.longLat.y,
            'lon': tree.longLat.x
        }
    })