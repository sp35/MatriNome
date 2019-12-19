from django.urls import path
from . import views as app_views

urlpatterns = [
    path('home', app_views.home, name='home'),
    path('', app_views.index, name='index')
]