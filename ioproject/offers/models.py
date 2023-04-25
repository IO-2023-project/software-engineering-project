from django.db import models

# Create your models here.
class ClientOrder(models.Model):
    registration_number = models.CharField(max_length=12)
    email = models.EmailField()
    status = models.IntegerField()


class MechanicOffer(models.Model):
    client_order = \
        models.ForeignKey(ClientOrder, on_delete=models.CASCADE) # delete all offers related to deleted order
    offer_content = models.TextField()
    offer_price = models.FloatField()

