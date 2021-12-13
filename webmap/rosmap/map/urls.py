from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('map', views.home, name='home'),
    path('map/api/upload', views.upload, name='upload'),
    path('map/marker/<slug:slug>/', views.marker_detail, name='marker_detail')
]