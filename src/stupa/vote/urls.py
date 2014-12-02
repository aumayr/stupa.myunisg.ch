from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^hashcodes/form/', views.hashcodes_form, name='hashcodes_form'),
    url(r'^hashcodes/print/', views.generate_hashcodes, name='generate_hashcodes'))
