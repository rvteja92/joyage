from django.conf.urls import include, url
from django.contrib import admin

from . import views


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^movie/(?P<movie_id>[0-9]+)$', views.movie, name='movie'),
]
