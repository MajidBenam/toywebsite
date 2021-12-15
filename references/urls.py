from django.urls import path

from . import views

## the path that I want is just nothing '', which means the route path (home page).
## views.index is the method we are connecting to Iinside views.py)
## But there is no index method in views just yet.
## the name = 'index' is to easily access this path. 
urlpatterns = [
	path('', views.references, name = 'references')
]