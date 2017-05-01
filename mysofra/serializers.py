from rest_framework import serializers
from mysofra.models import Product, mysofraMail

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'image_path', 'description')

class MailSerializer(serializers.ModelSerializer):
    class Meta:
        model = mysofraMail
        fields = ('id', 'subject', 'message', 'mail_from', 'mail_to', 'created')