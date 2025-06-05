from django.urls import path
from recipes.views import home

#dominio/recipes
urlpatterns = [
    path('', home), #Home   
]