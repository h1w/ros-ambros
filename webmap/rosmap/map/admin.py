from django.contrib import admin
from .models import Marker

class MarkerAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'gps', 'status', 'created_on',)
    list_filter = ('status',)
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Marker, MarkerAdmin)