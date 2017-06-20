from django.contrib import admin
from mysofra.models import Product, Mail, Category, Profile
# Register your models here.

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Mail)
admin.site.register(Profile)
