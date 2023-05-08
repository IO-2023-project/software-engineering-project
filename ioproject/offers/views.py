import re
from django.shortcuts import render
from django.http import HttpResponseNotAllowed

from ioproject.settings import DOMAIN_ADDRESS

from .models import ClientOrder
from .status import OrderStatus
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
                            status=OrderStatus.WAITING_FOR_OFFERS.value)
        order.save()
        order_id = order.pk

        mail.send_new_order_email(email, DOMAIN_ADDRESS + "orders/" + str(order_id) + "/view_offer", order_id, registration_number)
        # TODO: tutaj też ewentualne poprawki przy wysyłaniu emaila

        return render(request, "register.html", {"success": True})

    return render(request, "register.html", {"success": False})


def offers_list(request):
    if request.method == "GET": # TODO authorization
        offers = ClientOrder.objects.all()
        offers_dict = {}
        for offer in offers:
            offers_dict[offer.id] = {
                "registration_number": offer.registration_number,
                "email": offer.email,
                "status": str(OrderStatus(offer.status))
            }
        return render(request, "orders_list.html", {"offers": sorted(offers_dict.items())})

    return HttpResponseNotAllowed(['GET'])
