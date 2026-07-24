from django.urls import path
from . import views


app_name = 'home'
urlpatterns = [
    path('test/', views.test),
    path('', views.home_view, name='home'),
]