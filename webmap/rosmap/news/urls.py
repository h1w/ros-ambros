from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.news_list, name='news'),
    path('<slug:slug>/', views.new_detail, name='new_detail'),
]