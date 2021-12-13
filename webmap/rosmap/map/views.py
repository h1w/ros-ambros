from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
import os
import folium
from .models import Marker
import django.views.generic as generis
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt, requires_csrf_token
from base64 import decodestring
from django.utils.text import slugify
from unidecode import unidecode
from django.conf import settings
import datetime
from PIL import Image
import io
from .utils import randomize_slug

def home(request):
    template_name = 'home.html'
    m = folium.Map(location=[47.2243657, 38.9105216], tiles="OpenStreetMap", zoom_start=13)

    road_group = folium.FeatureGroup("Road")
    ambros_group = folium.FeatureGroup("Ambros")

    queryset = Marker.objects.order_by('-created_on')
    # queryset = Marker.objects.order_by('-created_on').filter(status=1)
    # queryset_drafts_only = Marker.objects.order_by('-created_on').filter(status=0)

    road_locations = []
    ambros_locations = []

    for marker in queryset:
        lat, lon = marker.gps.split(',')
        lat = lat.strip(' ')
        lon = lon.strip(' ')
        if marker.marker_type == 'ambros':
            ambros_locations.append((float(lat), float(lon)))
        else:
            road_locations.append((float(lat), float(lon)))

    for lat, lon in road_locations:
        marker = folium.Marker(
            location=[lat, lon],
            icon=folium.Icon(color='red'),
        )
        road_group.add_child(marker)

    for lat, lon in ambros_locations:
        marker = folium.Marker(
            location=[lat, lon],
            icon=folium.Icon(color='green'),
        )
        ambros_group.add_child(marker)

    m.add_child(road_group)
    m.add_child(ambros_group)

    folium.LayerControl().add_to(m)

    m=m._repr_html_()
    context = { 'my_map': m }
    ## rendering
    return render(request, template_name, context)

@csrf_exempt
def upload(request):
    template_name = "upload.html"
    context = {}

    if request.method == "POST":
        data = dict(request.POST.items())
        name = data['name']
        description = data['description']
        gps = data['gps']
        image_bytes = decodestring(data['image'].encode())
        request_type = data['request_type']
        
        img = Image.open(io.BytesIO(image_bytes))
        img = img.convert('RGB')
        img_format = 'jpg'
        image_abspath = '{}{}.{}'.format(settings.MEDIA_ROOT, datetime.datetime.now().strftime("%Y%m%d-%H%M%S-%f"), img_format)
        img.save(image_abspath)
        

        marker_instance = Marker()
        marker_instance.name = name
        marker_instance.description = description
        marker_instance.gps = gps
        marker_instance.image_path = image_abspath
        marker_instance.marker_type = request_type

        marker_instance.slug = randomize_slug(slugify(unidecode(marker_instance.name)))

        marker_instance.save()

        return HttpResponseRedirect(request.build_absolute_uri('/map/marker/' + marker_instance.slug))
    
    return render(request, template_name, context)

def marker_detail(request, slug):
    template_name = 'marker_detail.html'

    marker = get_object_or_404(Marker, slug=slug)

    context = {
        'name': marker.name,
        'description': marker.description,
        'gps': marker.gps,
        'image_path': marker.image_path,
        'marker_type': marker.marker_type
    }

    return render(request, template_name, context)