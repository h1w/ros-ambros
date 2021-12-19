from django.contrib import admin
from .models import Marker, ProblemRequest

class MarkerAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'gps', 'status', 'created_on',)
    list_filter = ('status',)
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

class ProblemRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'marker_slug', 'slug', 'created_on')
    search_fields = ['name', 'marker_slug', 'slug']

admin.site.register(Marker, MarkerAdmin)
admin.site.register(ProblemRequest, ProblemRequestAdmin)