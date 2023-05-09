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

    def status_enum(self):
        return OrderStatus(self.status)

class MechanicOffer(models.Model):
    client_order = \
        models.ForeignKey(ClientOrder, on_delete=models.CASCADE)  # delete all offers related to deleted order
    offer_content = models.TextField()
    offer_price = models.FloatField()
