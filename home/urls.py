from django.urls import path
from . import views


app_name = 'home'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('category/<int:id>/services/', views.ServicesView.as_view(), name='category_services'),
    path('service/<int:service_id>/', views.ServiceView.as_view(), name='service'),
]