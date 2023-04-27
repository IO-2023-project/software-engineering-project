from django.urls import path

from . import views


urlpatterns = [
    path('<int:id>', views.get_order),
    path('<int:id>/add_offer', views.add_offer, name="add_offer")
]