from django.db.models import query
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
import os
import folium
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
from django.contrib import messages

def home(request):
    template_name = 'moderation/home_page.html'
    context = {}
    return render(request, template_name, context)