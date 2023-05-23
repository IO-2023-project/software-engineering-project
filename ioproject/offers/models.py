from django.db import models

class OrderStatus(models.IntegerChoices):
    WAITING_FOR_OFFERS = 0, "Oczekiwanie na oferty mechanika"
    WAITING_FOR_CLIENT_DECISION = 1, "Oczekiwanie na decyzję klienta"
    WAITING_FOR_PARTS = 2, "Oczekiwanie na części"
    IN_PROGRESS = 3, "W trakcie naprawy"
    READY_TO_COLLECT = 4, "Gotowy do odbioru"
    COLLECTED = 5, "Odebrany"

# Create your models here.
class ClientOrder(models.Model):
    registration_number = models.CharField(max_length=12)
    email = models.EmailField()
    status = models.IntegerField(default=OrderStatus.WAITING_FOR_OFFERS, choices=OrderStatus.choices)
    chosen_offer = models.ForeignKey("MechanicOffer", on_delete=models.CASCADE, blank=True, null=True)

    def status_enum(self):
        return OrderStatus(self.status)

class OfferItem(models.Model):
    item_name = models.CharField(max_length=80) # not neccesarily unique
    #item_image = models.TextField() # can add this later
    item_description = models.TextField(default=None, null=True) # optional
    item_link = models.TextField(default=None, null=True) # optional
    item_price = models.FloatField()

    @classmethod
    def find_like(name):
        return OfferItem.objects.filter(item_name__icontains=name)

class MechanicOffer(models.Model):
    client_order = \
        models.ForeignKey(ClientOrder, on_delete=models.CASCADE)  # delete all offers related to deleted order
    offer_content = models.TextField()
    offer_items = models.ManyToManyField(OfferItem)
    work_price = models.FloatField()

    def total_price(self):
        return sum(item.item_price for item in self.offer_items.all()) + self.work_price
