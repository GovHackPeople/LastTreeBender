from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.conf import settings
from trees.models import random_tree
from django.contrib.gis import geos
import googlemaps

def index(request):
    template = loader.get_template('trees/index.html')
    return HttpResponse(template.render({}, request))

def view_map(request):
    address = __lookup_lat_long(request.GET['address'])
    tree = random_tree(address)
    directions = __get_directions(address, tree.longLat)
    steps = directions["legs"][0]["steps"]
    
    return JsonResponse({
        'metadata' : {
            'title': tree.treeType.commonName,
            'description': 'Also known as "%s"' % tree.treeType.scientificName,
            'imageUrl': tree.treeType.imageUrl,
            'numTreesInMelbourne': tree.treeType.scarcity,
        },
        'source': {
            'lat': address.y,
            'lon': address.x,
        },
        'dest': {
            'lat': tree.longLat.y,
            'lon': tree.longLat.x,
        },
        'bounds': directions['bounds'],
        'steps': steps
        
    })
    
def __lookup_lat_long(address):
    gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_GEOCODING_API)
    address_geo = gmaps.geocode(address)
    location = address_geo[0]["geometry"]["location"]
    return geos.Point(location["lng"], location["lat"])
    
def __get_directions(source_long_lat, dest_long_lat):
    gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_DIRECTIONS_API)
    directions_result = gmaps.directions(
        "%f,%f" % (source_long_lat.y, source_long_lat.x),
        "%f,%f" % (dest_long_lat.y, dest_long_lat.x),
        mode="walking",)
        
    return directions_result.pop()