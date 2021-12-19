from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('map.urls')),
    path('news/', include('news.urls')),
    path('aboutus/', TemplateView.as_view(template_name='aboutus.html'), name='aboutus'),
    path('volunteering/', TemplateView.as_view(template_name='volunteering.html'), name='volunteering'),
    path('instruction/', TemplateView.as_view(template_name='instruction.html'), name='instruction'),
    path('moderation/', include('moderation.urls')),
    path('donat/', TemplateView.as_view(template_name='donat.html'), name='donat'),
]
