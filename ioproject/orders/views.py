from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponseNotAllowed

from offers.models import ClientOrder, MechanicOffer


def get_order(request, id: int):
    if request.method == "GET":
        try:
            order = ClientOrder.objects.get(id=id)
            offers = MechanicOffer.objects.filter(client_order_id=id).values()
            return render(request, "order_details.html", {"success": True,
                                                          "editable": True,
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
        for i in range(len(data) // 2):
            content = data.get(f"offer_content_{i+1}")
            price = data.get(f"offer_price_{i+1}")
            offer = MechanicOffer(client_order=ClientOrder.objects.get(id=id), offer_content=content, offer_price=price)
            offer.save()
        return redirect(f"/orders/{id}")
    return render(request, "order_details.html", {"success": False,
                                                  "message": ""})

def view_offer(request, id: int):
    if request.method == "GET":
        try:
            order = ClientOrder.objects.get(id=id)
            offers = MechanicOffer.objects.filter(client_order_id=id).values()
            return render(request, "order_details.html", {"success": True,
                                                          "editable": False,
                                                          "order": order,
                                                          "offers": offers})
        except ObjectDoesNotExist:
            raise Http404()
            # return render(request, "offer_contents.html", {"success": False,
            #                                               "message": f"Zlecenie o numerze {id} nie istnieje."})
    return HttpResponseNotAllowed(["GET"],)
    # return render(request, "offer_contents.html", {"success": False,
    #                                               "message": ""})
