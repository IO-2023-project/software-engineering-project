from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render

from offers.models import ClientOrder


def get_order(request, id: int):
    if request.method == "GET":
        try:
            order = ClientOrder.objects.get(id=id)   # todo catch errors
            return render(request, "order_details.html", {"success": True, "order": order})
        except ObjectDoesNotExist:
            return render(request, "order_details.html", {"success": False, "id": id})
