from django.shortcuts import render

from .models import ClientOrder
from .status import OrderStatus

def register(request):
    if request.method == "POST":
        data = request.POST
        registration_number = data.get("registration_number")
        email = data.get("email")
        import re
        regex = re.compile(r"^[\w\-.]+@([\w-]+\.)+[\w\-]{2,4}$")
        if not regex.match(email):
            return render(request, "register.html", {"success": False, "invalid_email": True})

        order = ClientOrder(registration_number=registration_number, email=email,
                            status=OrderStatus.WAITING_FOR_OFFERS.value)
        order.save()

        return render(request, "register.html", {"success": True})

    return render(request, "register.html", {"success": False})
