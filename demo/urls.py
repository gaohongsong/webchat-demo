from django.conf.urls import url, include
from django.contrib import admin


from demo import views

urlpatterns = [
    url(r'^$', views.echo) 
]
