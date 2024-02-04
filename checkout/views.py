from django.shortcuts import render
from orders.models import Order
#from service.helpers import generateKey
from time import time  
from checkout.signals import create_ott_signal
import importlib 
from django.http.response import HttpResponse
# Create your views here.
def createOTT(request):
    
    order_id=request.POST['order_id']
    '''oinfo=Order.objects.get(pk=order_id)
    if(oinfo):
        device_id=oinfo['device_id']
        customer_id=oinfo['customer_id']
        k=generateKey(order_id)
   '''
    create_ott_signal.send(None,order_id=order_id)
def payment_view(request):
    #key=request.POST['order_id']
    param2='payment.gateways.{}.hooks'.format('cod')
    module=importlib.import_module(param2)
    return module.paymentForm(request)
def success(request):
     return HttpResponse("SUCCESS")
def fail(request):
     return HttpResponse("fAIL")

    