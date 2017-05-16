from mysofra.models import Product, Mail
from mysofra.serializers import ProductSerializer, MailSerializer
from rest_framework import generics
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.shortcuts import render, redirect
import braintree
from django.contrib import messages

TRANSACTION_SUCCESS_STATUSES = [
    braintree.Transaction.Status.Authorized,
    braintree.Transaction.Status.Authorizing,
    braintree.Transaction.Status.Settled,
    braintree.Transaction.Status.SettlementConfirmed,
    braintree.Transaction.Status.SettlementPending,
    braintree.Transaction.Status.Settling,
    braintree.Transaction.Status.SubmittedForSettlement
]

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

def new_checkout(request):
    if request.method == 'POST':
        client_token = braintree.ClientToken.generate()
        amount = request.POST.get('amount')
        return render(request, 'checkouts/new.html', {'client_token':client_token,'amount':amount})
    else:
        client_token = braintree.ClientToken.generate()
        amount = 13.30
        return render(request, 'checkouts/new.html', {'client_token':client_token,'amount':amount})

def show_checkout(request, transaction_id):
    transaction = braintree.Transaction.find(transaction_id)
    result = {}
    
    if transaction.status in TRANSACTION_SUCCESS_STATUSES:
        result = {
            'header': 'Sweet Success!',
            'icon': 'success',
            'message': 'Your test transaction has been successfully processed. See the Braintree API response and try again.'
        }
    else:
        result = {
            'header': 'Transaction Failed',
            'icon': 'fail',
            'message': 'Your test transaction has a status of ' + transaction.status + '. See the Braintree API response and try again.'
        }

    return render(request, 'checkouts/show.html', {'result_set':result, 'transaction':transaction})

def create_checkout(request):
    if request.method == 'POST':

        result = braintree.Transaction.sale({
            'amount': request.POST.get('amount'),
            'payment_method_nonce': request.POST.get('payment_method_nonce'),
            'options': {
                "submit_for_settlement": True
            }
        })
        if result.is_success or result.transaction:
            return redirect('/checkouts/'+result.transaction.id +'/',transaction_id=result.transaction.id)
        else:
            for x in result.errors.deep_errors: messages.error(request, 'Error: %s: %s' % (x.code, x.message))
            return redirect('/checkouts/new/')