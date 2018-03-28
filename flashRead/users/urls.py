from django.conf.urls import url, include, patterns
from django.views.generic.edit import CreateView

from django.contrib.auth.views import login, logout

from users import views

urlpatterns = [
    url(r'^profile/$', views.profile, name="profile"),
    url(r'^favouriteBooks/$', views.favouriteBooks, name="favouriteBooks"),
    url(r'^deleteFavourite/(?P<book_id>[0-9]+)/$', views.deleteFavourite, name="deleteFavourite"),
    url(r'^bookmark/$', views.bookmarkChapters, name="bookmarkChapters"),
    url(r'^deleteBookmark/(?P<chapter_id>[0-9]+)/$', views.deleteBookmark, name="deleteBookmark"),
    url(r'^edit_profile/$', views.edit_profile, name="edit_profile"),
    
    url(r'^register_success/$', views.register_success, name="register_success"),
    url(r'^register/', views.register, name="register"),
               
    url(r'^accounts/', include('django.contrib.auth.urls'),  name="account"),
    url(r'^login/$', login, {'template_name': 'users/login.html'}, name="login"),
    url(r'^logout/$', logout, {'template_name': 'users/logout.html'}, name="logout"),
]
