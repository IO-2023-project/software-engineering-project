from django.urls import path

from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('list', views.offers_list, name='orders_list')
]