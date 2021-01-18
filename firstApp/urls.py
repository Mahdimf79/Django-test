from django.conf.urls import url
from . import views

app_name = 'firstApp'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^/(?P<pk>[0-9]+)/$', views.detail, name='detail'),
    url(r'^/(?P<pk>[0-9]+)/results$', views.results, name='results'),
    url(r'^/(?P<pk>[0-9]+)/vote$', views.vote, name='vote'),
]
