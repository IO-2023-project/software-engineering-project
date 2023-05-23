import re
from django.shortcuts import render, redirect
from django.http import HttpResponseNotAllowed

from ioproject.settings import DOMAIN_ADDRESS

from .models import ClientOrder, OrderStatus, OfferItem, MechanicOffer
# from ioproject.mail.send_email import send_new_order_email
import mail.send_email as mail


def register(request):
    if request.method == "POST":
        data = request.POST
        registration_number = data.get("registration_number")
        email = data.get("email")
        regex = re.compile(r"^.+@.+\..+$")
        if not regex.match(email):
            return render(request, "register.html", {"success": False, "invalid_email": True})

        order = ClientOrder(registration_number=registration_number, email=email,
                            status=OrderStatus.WAITING_FOR_OFFERS.value, chosen_offer=None)
        order.save()
        order_id = order.pk

        mail.send_new_order_email(email, DOMAIN_ADDRESS + "orders/" + str(order_id) + "/view_offer", order_id, registration_number)
        # TODO: tutaj też ewentualne poprawki przy wysyłaniu emaila

        return render(request, "register.html", {"success": True})

    return render(request, "register.html", {"success": False})


def offers_list(request):
    if request.method == "GET": # TODO authorization
        orders = ClientOrder.objects.all()
        return render(request, "orders_list.html", {"orders": sorted(list(orders), key=lambda order: order.id)})

    return HttpResponseNotAllowed(['GET'])


def add_item(request, id: int):
    if request.method == "POST":
        data = request.POST
        try:
            offer = MechanicOffer.objects.get(id=id)
            item = OfferItem(item_name=data["name"], item_description=data["description"], item_link=data["link"], item_price=data["price"])
            item.save()
            offer.offer_items.add(item)
            offer.save()
            return redirect(f"/orders/{offer.client_order.id}")
        except Exception as e:
            return render(request, "register.html", {"success": False, "message": e})
