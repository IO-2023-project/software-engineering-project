from django.shortcuts import render

from offers.models import ClientOrder


def get_order(request, id: int):
    if request.method == "GET":
        order = ClientOrder.objects.get(id=id)   # todo catch errors
        return render(request, "order_details.html", {"success": True, "order": order})

    return render(request, "order_details.html", {"success": False})
