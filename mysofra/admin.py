from django.contrib import admin
from mysofra.models import Product, Mail, Category
# Register your models here.

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Mail)
