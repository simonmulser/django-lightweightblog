from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^articles/', include('articles.urls', namespace="articles")),
    url(r'^backend/', include('backend.urls', namespace="backend")),
    url(r'^accounts/', include('accounts.urls', namespace="accounts")),
)
