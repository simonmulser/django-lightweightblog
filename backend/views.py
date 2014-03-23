from django.shortcuts import render
from articles.models import Article
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from django.forms import ValidationError

class IndexView(generic.ListView):
    template_name = 'backend/index.html'
    context_object_name = 'latest_articles'
    
    def get_queryset(self):
        return Article.objects.order_by('-publication')[:5]  # @UndefinedVariable

class DetailView(generic.DetailView):
    model = Article
    template_name ='backend/detail.html'

def create(request):
    return render(request, 'backend/create.html')

def save(request):
    try:
        article = Article(heading=request.POST['heading'], content=request.POST['content'])
        if(article.publication == None):
            article.publication = timezone.now()
        article.full_clean()
        article.save()
    except (KeyError, ValidationError):
        # Redisplay the poll voting form.
        return render(request, 'backend/create.html', {
            'error_message': "Error: Insert correct values",
        })
    else:
        return HttpResponseRedirect(reverse("backend:index"))
