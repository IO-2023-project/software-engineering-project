import re
from django.shortcuts import render

from .models import ClientOrder
from .status import OrderStatus
from ..mail.send_email import send_new_order_email

CUSTOMER_LINK = "TODO"


#  TODO: dodać poprawny link do strony ze zleceniem klienta


def register(request):
    if request.method == "POST":
        data = request.POST
        registration_number = data.get("registration_number")
        email = data.get("email")
        regex = re.compile(r"^[\w\-.]+@([\w-]+\.)+[\w\-]{2,4}$")
        if not regex.match(email):
            return render(request, "register.html", {"success": False, "invalid_email": True})

        order = ClientOrder(registration_number=registration_number, email=email,
                            status=OrderStatus.WAITING_FOR_OFFERS.value)
        order.save()
        order_id = order.pk

        send_new_order_email(email, CUSTOMER_LINK + str(order_id), order_id, registration_number)

        return render(request, "register.html", {"success": True})

    return render(request, "register.html", {"success": False})
