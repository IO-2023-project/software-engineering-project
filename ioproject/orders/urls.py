from django.urls import path

from . import views

urlpatterns = [
    path('<int:id>', views.get_order),
    path('<int:id>/add_offer', views.add_offer, name="add_offer"),
    path('<int:id>/view_offer', views.view_offer, name="view_offer"),
    path('<int:order_id>/choose_offer/<int:offer_id>', views.choose_offer, name="choose_offer"),
    path('<int:id>/change_status/', views.change_status, name="change_status")
]