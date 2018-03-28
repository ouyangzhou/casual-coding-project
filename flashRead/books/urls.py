from django.conf.urls import url

from books import views

urlpatterns = [
    #url(r'^/flashRead/$', views.index, name='index'),
    url(r'^$', views.index, name='index'),
    url(r'^result/$', views.search, name='search'),
    url(r'^goToAdvSearch/$', views.goToAdvSearch, name='goToAdvSearch'),
    url(r'^advSearch/$', views.advSearch, name='advSearch'),
    url(r'^(?P<book_id>[0-9]+)/$', views.login_user_view, name='login_user_view'),
    url(r'^(?P<book_id>[0-9]+)/favourite/$', views.favourite, name='favourite'),
    url(r'^(?P<book_id>[0-9]+)/vote/$', views.vote, name='vote'),
]
