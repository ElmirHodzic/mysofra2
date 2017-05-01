from django.db import models

PRODUCT_CHOICES = [("1","Huhnerfleisch"), ("2","Rindfleisch")];

class Product(models.Model):
    name = models.CharField(max_length=100, blank=True, default='')
    price = models.DecimalField(max_digits=5, decimal_places=2)
    image_path = models.CharField(max_length=100, blank=True, default='sirloin.png')
    description = models.CharField(max_length=2000, blank=True, default='Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc eget mollis urna, imperdiet malesuada eros. Nunc eget mollis urna, imperdiet malesuada eros.')
    category = models.CharField(choices=PRODUCT_CHOICES, max_length=100)


class mysofraMail(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    subject = models.CharField(max_length=100, blank=True, default='')
    message = models.TextField()
    mail_from = models.CharField(default='checkouts@mysofra.at', max_length=100)
    mail_to = models.CharField(default='orders@mysofra.at', max_length=100)

    class Meta:
        ordering = ('created',)