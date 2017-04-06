from mysofra.models import Product, mysofraMail
from mysofra.serializers import ProductSerializer, MailSerializer
from rest_framework import generics
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail

class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class MailList(APIView):
    """
    List all mails, or create a new mail.
    """
    def get(self, request, format=None):
        mails = mysofraMail.objects.all()
        serializer = MailSerializer(mails, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = MailSerializer(data=request.data)
        if serializer.is_valid():
            mail_from = 'checkouts@mysofra.at'#request.data['mail_from'] if 'mail_from' in request.data else 
            mail_to = request.data['mail_to'] if 'mail_to' in request.data else 'orders@mysofra.at'
            send_mail(request.data['subject'], request.data['message'], mail_from, [mail_to])            
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MailDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return mysofraMail.objects.get(pk=pk)
        except mysofraMail.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        mail = self.get_object(pk)
        serializer = MailSerializer(mail)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        mail = self.get_object(pk)
        serializer = MailSerializer(mail, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        mail = self.get_object(pk)
        mail.delete()