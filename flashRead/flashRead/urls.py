
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import RedirectView
from django.core.urlresolvers import reverse_lazy
from users import views

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^users/', include('users.urls', namespace='users')),   
    url(r'^books/', include('books.urls', namespace='books')),
    url(r'^mycontent/', include('addContent.urls', namespace='addContent')),
    url(r'^chapters/', include('chapters.urls', namespace='chapters')),
    url(r'^home/', include('home.urls', namespace='home')),
    url(r'^$', RedirectView.as_view(url=reverse_lazy('home:index')), name='go-to-home'),
)

