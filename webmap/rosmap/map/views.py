from django.db.models import query
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
    template_name = 'map/map.html'
    # tiles = "Stamen Terrain" - default
    m = folium.Map(location=[47.2243657, 38.9105216], tiles="OpenStreetMap", zoom_start=13)

    road_group = folium.FeatureGroup("Road")
    ambros_group = folium.FeatureGroup("Ambros")

    queryset = Marker.objects.order_by('-created_on')
    # queryset = Marker.objects.order_by('-created_on').filter(status=1)
    # queryset_drafts_only = Marker.objects.order_by('-created_on').filter(status=0)

    tooltip = "Информация"

    for marker in queryset:
        lat, lon = marker.gps.split(',')
        lat = float(lat.strip(' '))
        lon = float(lon.strip(' '))
        if marker.marker_type == 'ambros':
            marker = folium.Marker(
                location=[lat,lon],
                icon=folium.Icon(color='green'),
                popup=f"""<img width="500px" src="{settings.MEDIA_URL + marker.image_path}" alt="{marker.slug}"/><br><p>{marker.description}</p>""",
                tooltip=tooltip,
            )
            ambros_group.add_child(marker)
        else:
            marker = folium.Marker(
                location=[lat, lon],
                icon=folium.Icon(color='red'),
                popup=f"""<img width="500px" src="{settings.MEDIA_URL + marker.image_path}" alt="{marker.slug}"/><br><p>{marker.description}</p>""",
                tooltip=tooltip,
            )
            road_group.add_child(marker)

    m.add_child(road_group)
    m.add_child(ambros_group)

    folium.LayerControl().add_to(m)

    m=m._repr_html_()
    context = { 
        'my_map': m,
    }

    return render(request, template_name, context)

@csrf_exempt
def upload(request):
    template_name = "map/upload.html"
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
        nametime = datetime.datetime.now().strftime("%Y%m%d-%H%M%S-%f")
        image_abspath = '{}{}.{}'.format(settings.MEDIA_ROOT, nametime, img_format)
        img.save(image_abspath)
        

        marker_instance = Marker()
        marker_instance.name = name
        marker_instance.description = description
        marker_instance.gps = gps
        marker_instance.image_path = "{}.{}".format(nametime, img_format)
        marker_instance.marker_type = request_type

        marker_instance.slug = randomize_slug(slugify(unidecode(marker_instance.name)))

        marker_instance.save()

        return HttpResponseRedirect(request.build_absolute_uri('/map/marker/' + marker_instance.slug))
    
    return render(request, template_name, context)

def marker_detail(request, slug):
    template_name = 'map/marker_detail.html'

    marker = get_object_or_404(Marker, slug=slug)

    context = {
        'name': marker.name,
        'description': marker.description,
        'gps': marker.gps,
        'image_path': settings.MEDIA_URL + marker.image_path,
        'marker_type': marker.marker_type
    }

    return render(request, template_name, context)