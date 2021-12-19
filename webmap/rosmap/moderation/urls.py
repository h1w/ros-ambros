from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='moderation_page'),
    # path('map/api/upload', views.upload, name='upload'),
    # path('map/marker/<slug:slug>/', views.marker_detail, name='marker_detail'),
    # path('map/marker/<slug:slug>/problemrequest', views.problem_request, name='problem_request'),
]