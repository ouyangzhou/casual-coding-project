from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.template.response import TemplateResponse

# Create your views here.
def index(request):
	#template = loader.get_template('home/index.html')
	#from https://docs.djangoproject.com/en/dev/ref/template-response/
	response = TemplateResponse(request, 'home/index.html', {})
	#response.add_post_render_callback(my_render_callback)

	return response