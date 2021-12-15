from django.shortcuts import get_object_or_404, render
from .models import New

def news_list(request):
    template_name = 'news/news.html'
    context = {}
    queryset = New.objects.order_by('-created_on').filter(status=1)
    queryset_drafts_only = New.objects.filter(status=0)
    
    if request.method == 'GET':
        context['news_list'] = queryset
    
    return render(request, template_name, context)

def new_detail(request, slug):
    template_name = 'news/new_detail.html'
    
    new = get_object_or_404(New, slug=slug)

    context = {
        'new': new
    }

    return render(request, template_name, context)