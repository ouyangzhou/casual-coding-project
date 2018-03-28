from django.conf.urls import patterns, url

from addContent import views

urlpatterns = patterns('',
	url(r'^myWorks/$', views.myWorks, name='myWorks'),
	url(r'^addWork/$', views.addBook, name='addBook'),
	url(r'^editWork/(?P<bid>\d+)/$', views.editBook, name='editBook'),
	url(r'^work/(?P<bid>\d+)/addChapter/$', views.addChapter, name='addChapter'),
	url(r'^work/(?P<bid>\d+)/editChapter/(?P<chid>\d+)/$', views.editChapter, name='editChapter')
)