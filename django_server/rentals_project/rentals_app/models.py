from django.db import models
from django.contrib.auth.models import User

# Create your models here.



class FavoriteOffer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    offer_id = models.CharField(max_length=50)
    link = models.URLField()
    image_link = models.URLField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rent = models.DecimalField(max_digits=10, decimal_places=2, default=-1)
    address = models.CharField(max_length=255)
    rooms = models.IntegerField()
    surface = models.DecimalField(max_digits=6, decimal_places=2)
    website = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user.username}'s favorite offer {self.offer_id}"
