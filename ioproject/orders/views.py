from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponseNotAllowed

from offers.models import ClientOrder, MechanicOffer, OrderStatus, OfferItem

import mail.send_email as mail

STATUS_LIST = [status for status in OrderStatus]


def get_order(request, id: int):
    if request.method == "GET":
        try:
            order = ClientOrder.objects.get(id=id)
            offers = MechanicOffer.objects.filter(client_order_id=id)
            ids = [offer.id for offer in offers]
            items = OfferItem.objects.filter(mechanicoffer__id__in=ids)
            sorted_items = {}
            offer_prices = {offer.id: offer.total_price() for offer in offers}
            for item in items:
                mechanic_offers = MechanicOffer.objects.filter(offer_items__id=item.id)
                for mechanic_offer in mechanic_offers:
                    sorted_items[mechanic_offer.id] = sorted_items.get(mechanic_offer.id, []) + [item]

            return render(request, "order_details.html", {"success": True,
                                                          "editable": True,
                                                          "order": order,
                                                          "offers": offers,
                                                          "order_items": sorted_items,
                                                          "offer_prices": offer_prices,
                                                          "status_list": STATUS_LIST})
        except ObjectDoesNotExist:
            return render(request, "order_details.html", {"success": False,
                                                          "message": f"Zlecenie o numerze {id} nie istnieje."})
    return render(request, "order_details.html", {"success": False,
                                                  "message": ""})


def add_offer(request, id: int):
    if request.method == "POST":
        data = request.POST
        for i in range(len(data) // 2):
            content = data.get(f"offer_content_{i + 1}")
            price = data.get(f"offer_price_{i + 1}")
            offer = MechanicOffer(client_order=ClientOrder.objects.get(id=id), offer_content=content, work_price=price)
            offer.save()
        return redirect(f"/orders/{id}")
    return render(request, "order_details.html", {"success": False,
                                                  "message": ""})


def view_offer(request, id: int):
    if request.method == "GET":
        try:
            order = ClientOrder.objects.get(id=id)
            offers = MechanicOffer.objects.filter(client_order_id=id)
            return render(request, "order_details.html", {"success": True,
                                                          "editable": False,
                                                          "order": order,
                                                          "offers": offers,
                                                          "status_list": STATUS_LIST})
        except ObjectDoesNotExist:
            raise Http404()
            # return render(request, "offer_contents.html", {"success": False,
            #                                               "message": f"Zlecenie o numerze {id} nie istnieje."})
    return HttpResponseNotAllowed(["GET"], )
    # return render(request, "offer_contents.html", {"success": False,
    #                                               "message": ""})


def choose_offer(request, order_id: int, offer_id: int):
    if request.method == "POST":
        try:
            order = ClientOrder.objects.get(id=order_id)
            order.status = OrderStatus.WAITING_FOR_PARTS.value
            order.chosen_offer = MechanicOffer.objects.get(id=offer_id)
            order.save()
            mail.email_about_chosen_offer(order_id, offer_id)
            return redirect(f"/orders/{order_id}/view_offer")
        except ObjectDoesNotExist:
            raise Http404()
    return HttpResponseNotAllowed(["POST"], )


def change_status(request, id: int):
    if request.method == "POST":
        data = request.POST
        try:
            new_status = data.get("status")
            order = ClientOrder.objects.get(id=id)
            order.status = int(new_status)
            order.save()
            if order.status == OrderStatus.WAITING_FOR_CLIENT_DECISION.value:
                mail.send_email_about_created_offers(id)
            if order.status == OrderStatus.READY_TO_COLLECT.value:
                mail.finished_order_email(id)

            return redirect(f"/orders/{id}")
        except ObjectDoesNotExist:
            return render(request, "order_details.html", {"success": False,
                                                          "message": f"Zlecenie o numerze {id} nie istnieje."})
