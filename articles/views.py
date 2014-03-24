from articles.models import Article
from django.views import generic
from django.utils import timezone


class IndexView(generic.ListView):
    template_name = 'articles/index.html'
    context_object_name = 'latest_articles'
    
    def get_queryset(self):
        return Article.objects.filter(
            publication__lte=timezone.now()).order_by('-publication')[:10]  # @UndefinedVariable

class DetailView(generic.DetailView):
    model = Article
    template_name ='articles/detail.html'
    
    def get_queryset(self):
        return Article.objects.filter(publication__lte=timezone.now())