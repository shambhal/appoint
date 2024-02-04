from django.shortcuts import render,redirect
from checkout.models import CheckoutKey
from .models import COD
from orders.models import Order
from django.urls import reverse
# Create your views here.
def checkpayment(request):
     ot= request.POST.get('ott','')
     qs=CheckoutKey.objects.all().filter('key',ot)
     if(qs.exists()):
          record=qs.first()
          order_id=record.order_id
          obj=COD.objects.get(pk=1)
          ord=Order.objects.get(id=order_id)
          ord.status='COMPLETE'
          ord.save()
          return redirect(reverse('checkout:success'))
     return redirect(reverse('checkout:failure'))