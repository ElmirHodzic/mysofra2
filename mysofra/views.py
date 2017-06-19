# -*- coding: utf-8 -*-
from mysofra.models import Product, Mail, Category, Profile
from mysofra.serializers import ProductSerializer, MailSerializer, CategorySerializer, ProfileSerializer
from rest_framework import generics
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.shortcuts import render, redirect
import braintree
from django.contrib import messages
import json
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http import HttpResponse, JsonResponse

TRANSACTION_SUCCESS_STATUSES = [
    braintree.Transaction.Status.Authorized,
    braintree.Transaction.Status.Authorizing,
    braintree.Transaction.Status.Settled,
    braintree.Transaction.Status.SettlementConfirmed,
    braintree.Transaction.Status.SettlementPending,
    braintree.Transaction.Status.Settling,
    braintree.Transaction.Status.SubmittedForSettlement
]

class ProfileList(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    
def make_mail(dic, num):
    mail =  'You have a new online({0}) order from,\n\n'.format(num);
    mail += 'Name:       {0} {1}\n'.format(dic['name'], dic['lname']);
    mail += 'Address:    {0}\n'.format(dic['address'])
    mail += 'Email:      {0}\n'.format(dic['email'])
    mail += 'Telephone:  {0}\n'.format(dic['number'])
    mail += 'Payment:    {0}\n'.format(dic['payment'])
    mail += 'Order date: {0}\n\n\n'.format(dic['date'])
    mail += '{:->56}'.format('\n')
    mail += '|Nr.  |    Product name    |    Price    |  Quantity  |\n'
    mail += '{:->56}'.format('\n')

    for x in xrange(len(dic['products'])):
        p = Product.objects.get(pk=dic['products'][x])
        mail += u'|{:>5}|    {:>12}    |    {:>7}  |  {:>8}  |\n'.format(x, p.name, p.price, dic['quantities'][x])
        mail += '{:->56}'.format('\n')
    
    mail += '| AMOUNT {:>45}|\n'.format(dic['amount'])
    mail += '{:->56}'.format('\n\n')
    mail += '{:%d.%m.%Y %H:%M}\n'.format(datetime.now())
    mail += 'mysofra.at team'

    return mail;

def mail_to_consumer(dic, num):
    mail = """<table><tr col align="center"><td colspan="3"><b>BETREFFZEILE: MySofra.at - Bestellnummer {0}</b></td><td>""".format(num)
    mail += """</td><td>  </td></tr><tr><td colspan="3"> Guten Tag {title} {lname},</td></tr><tr><td colspan="3">Herzlichen Dank für Ihre Bestellung bei <a href="https://www.mysofra.at/home"/>mysofra.at</a>. Mit dieser E-Mail ist der Kaufvertrag zustande gekommen. Wir bearbeiten Ihre Bestellung schnellstmöglich. Sie werden die bestellte Ware an dem im Bestellformular  angegebenen Tag erhalten.   </td><td> </td><td>  </td></tr><tr><td bgcolor="#0000ff"colspan="3"><h3><font color="white">Adresse</font></h3></td></tr><tr><td>Emailadresse: {email}</td></tr><tr><td>Telefonnummer: {number}</td></tr><tr><td>Lieferdatum: {date}</td></tr><tr><td><b>Lieferadresse</b></td><td><b>Rechnungsadresse</b></td></tr><tr> <td>{title} {name} {lname}<br />{address}<br />Österreich</td><td>{stitle} {sname} {slname}<br />{saddress}<br />Österreich</td></tr><tr><td><b /></td></tr><tr><td><b>Gewählte Zahlart:</b> {payment} </td></tr><tr><td><b />Bemerkungen</td></tr><tr><td bgcolor="#0000ff" colspan="3"><h3><font color="white">Zusammenfassung der Bestellung</font></h3> </td></tr><tr bgcolor="#C0C0C0"><td width="20%"><b>Anzahl</b>	   </td><td width="70%"> <b>Produkt</b> </td><td width="10%"> <b>Preis</b>  </td></tr>""".format(**dic);
    for x in xrange(len(dic['products'])):
    	p = Product.objects.get(pk=dic['products'][x]);
    	mail += """<tr><td>{0}</td><td><b>{1}</b><br />Wird frisch geliefert, soll kühl gelagert werden.</td><td>{2}</td></tr>""".format(dic['quantities'][x], p.name.encode('utf-8'), p.price);
    mail += """<tr><td><b />Total Bestellwert (inkl. MWST)</td><td></td><td><b />EUR {0} </td></tr><tr><td bgcolor="#0000ff" colspan="3"><h3><font color="white">ZUSTELLUNG IST KOSTENLOS</font></h3></td></tr><tr><td colspan="3"> Es gelten unsere Allgemeinen Geschäftsbedingungen. Verbraucher haben ein 14-tägiges Rückgaberecht.</td></tr><td></td><td></td> <br /><tr><td colspan="3">Haben Sie Fragen zu Ihrer Bestellung?<br />Sie erreichen unseren Kundenservice von Mo-Fr von 10-13 Uhr und 14-19 Uhr. <br />Tel.: +43 (1) 890 05 31 - 0<br />Mail: <a href="info@mysofra.at" target="top"> info@mysofra.at </a>  <br />Bitte nennen Sie Ihren Namen, Anschrift, Stadt und Bestell-Nr.<td></td><td></td></tr><tr><td colspan="3">Vielen Dank,<br />Ihr MySofra Serviceteam</td><td></td><td></td></tr></table>""".format(dic['amount']);
    return mail;

class MailList(APIView):
    """
    List all mails, or create a new mail.
    """
    def get(self, request, format=None):
        mails = Mail.objects.all()
        serializer = MailSerializer(mails, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = MailSerializer(data=request.data)
        if serializer.is_valid():
            mail_from = 'team@mysofra.at'#request.data['mail_from'] if 'mail_from' in request.data else 
            mail_to = request.data['mail_to'] if 'mail_to' in request.data else 'order@mysofra.at'
            dic = json.loads(request.data['message']);             
            serializer.save()
            send_mail(request.data['subject'], make_mail(dic, serializer.data['id']), mail_from, [mail_to]);
            msg = mail_to_consumer(dic, serializer.data['id']);	
            send_mail('Your order is ready', msg, mail_from, [dic['email']], html_message = msg)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MailDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return Mail.objects.get(pk=pk)
        except Mail.DoesNotExist:
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

def new_checkout(request, pk):
    if request.method == 'POST':
        client_token = braintree.ClientToken.generate()
        amount = request.POST.get('amount')
        return render(request, 'checkouts/new.html', {'client_token':client_token,'amount':amount})
    else:
        client_token = braintree.ClientToken.generate()
        m = Mail.objects.get(pk=pk)
        return render(request, 'checkouts/new.html', {'client_token':client_token,'amount':m.amount})

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

@csrf_exempt
def logintest(request):
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request)
            mail = data['email']
            profile = Profile.objects.get(email=mail);
            if(data['password'] != profile.password):
                print(data['password'] + " " + profile.password)
                return HttpResponse(status=404);
            serializer = ProfileSerializer(profile);
            return JsonResponse(serializer.data, safe=False);
        except Profile.DoesNotExist:
            return HttpResponse(status=404);
    else:
        return HttpResponse(status=404);
