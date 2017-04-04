from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100, blank=True, default='')
    price = models.DecimalField(max_digits=5, decimal_places=2)
    image_path = models.CharField(max_length=100, blank=True, default='sirloin.png')
    description = models.CharField(max_length=2000, blank=True, default='Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc eget mollis urna, imperdiet malesuada eros. Nunc eget mollis urna, imperdiet malesuada eros.')
