from django.conf.urls import patterns, url

from backend import views

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^create$', views.create, name='create'),
    url(r'^save$', views.save, name='save'),
    url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),

)