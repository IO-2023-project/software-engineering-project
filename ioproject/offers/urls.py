from django.urls import path

from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('list', views.offers_list, name='orders_list'),
    path('<int:id>/add-item/', views.add_item, name="add_item")
]