from django.conf.urls import url
from . import views

app_name = 'firstApp'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<pk>[0-9]+)/results$', views.results, name='results'),
    url(r'^(?P<pk>[0-9]+)/vote$', views.vote, name='vote'),
    url(r'^setQuestion$', views.setQuestion, name='setQuestion'),
    url(r'^create_question$', views.create_question, name='create_question'),
    url(r'^(?P<pk>[0-9]+)/setChoice$', views.setChoice, name='setChoice'),
    url(r'^(?P<pk>[0-9]+)/create_choice$', views.create_choice, name='create_choice'),
    url(r'^register/$', views.register, name='register'),
    url(r'^register_set/$', views.register_set, name='register_set'),
    url(r'^login/$', views.login, name='login'),
    url(r'^login_set/$', views.login_set, name='login_set'),
    url(r'^logout/$', views.logout, name='logout'),
]
