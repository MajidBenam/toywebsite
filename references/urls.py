from django.urls import path

from . import views

from .views import static_file_view
from django.views.generic.base import TemplateView


## the path that I want is just nothing '', which means the route path (home page).
## views.index is the method we are connecting to Iinside views.py)
## But there is no index method in views just yet.
## the name = 'index' is to easily access this path. 
urlpatterns = [
	path('', views.references, name = 'references'),
    #path('<slug:html_file_name>/', TemplateView.as_view(template_name='static/{html_file_name}'), name='static'),
	path('<str:file_name>', static_file_view, name='static_file_view'),

	
]
