from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render

from offers.models import ClientOrder, MechanicOffer
from offers.status import OrderStatus


def get_order(request, id: int):
    if request.method == "GET":
        try:
            order = ClientOrder.objects.get(id=id)
            offers = MechanicOffer.objects.filter(client_order_id=id).values()
            return render(request, "order_details.html", {"success": True,
                                                          "order": order,
                                                          "offers": offers})
        except ObjectDoesNotExist:
            return render(request, "order_details.html", {"success": False,
                                                          "message": f"Zlecenie o numerze {id} nie istnieje."})
    return render(request, "order_details.html", {"success": False,
                                                  "message": ""})


def add_offer(request, id: int):
    if request.method == "POST":
        data = request.POST
        content = data.get("offer_content")
        price = data.get("offer_price")
        order = ClientOrder.objects.filter(id=id).values()[0]
        order.update(status=OrderStatus.WAITING_FOR_CLIENT_DECISION.value)
        offer = MechanicOffer(client_order=ClientOrder.objects.get(id=id), offer_content=content, offer_price=price)
        offer.save()
        offers = MechanicOffer.objects.filter(client_order_id=id).values()
        return render(request, "order_details.html", {"success": True,
                                                      "order": order,
                                                      "offers": offers})
    return render(request, "order_details.html", {"success": False,
                                                  "message": ""})

