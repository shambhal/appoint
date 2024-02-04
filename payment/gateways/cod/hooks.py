from payment.models import Payment
from .models import COD
from django.shortcuts import render

def getQuote():
        
        obj=COD.objects.get(pk=1)
        if(not obj):
         return {}
        if(obj.status==0):
          
          return {}
        
        context={'name':'cod','title':'Cash on delivery','sort_order':obj.sort_order}
        return context
def getLink():
    ob= obj=COD.objects.get(pk=1)  
    if(ob is None) : 
     return '/admin/cod/cod/add'
    else:
       return '/admin/cod/cod/1/change'
    
def paymentForm(request,extra):
          action='payment/checkout/success'
          return render(request,'front/payment.html',{'ott':extra['key']})