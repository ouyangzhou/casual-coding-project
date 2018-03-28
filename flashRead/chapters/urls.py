from django.conf.urls import url

from chapters import views

urlpatterns = [
    #url(r'^$', views.index, name='index'),
    url(r'^(?P<chapter_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<chapter_id>[0-9]+)/bookmark/$', views.bookmark, name='bookmark'),
    
]
