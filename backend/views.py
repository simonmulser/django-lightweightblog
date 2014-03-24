from django.shortcuts import render
from articles.models import Article
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.http import Http404
from django.shortcuts import get_object_or_404
from django import forms
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator




class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article

class IndexView(generic.ListView):
    template_name = 'backend/index.html'
    context_object_name = 'latest_articles'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return generic.ListView.dispatch(self, request, *args, **kwargs)
    
    def get_queryset(self):
        return Article.objects.order_by('-publication')  # @UndefinedVariable
    
class DetailView(generic.DetailView):
    model = Article
    template_name ='backend/detail.html'
        
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return generic.DetailView.dispatch(self, request, *args, **kwargs)

@login_required   
def delete_article(request):
    try:
        article = Article.objects.get(pk=request.POST['pk'])
        article.delete()
    except (Article.DoesNotExist, KeyError):
        raise Http404
    return HttpResponseRedirect(reverse("backend:index"))

@login_required    
def edit_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    form = ArticleForm(request.POST or None, instance=article)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse("backend:index"))
    return render(request, 'backend/form.html', {'form':form})

@login_required   
def create_article(request):
    form = ArticleForm(request.POST or None)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse("backend:index"))
    return render(request, 'backend/form.html', {'form':form})

