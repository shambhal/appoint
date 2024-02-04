from django.http.response import JsonResponse,HttpResponse
from django.shortcuts import render,redirect
from django.urls import reverse
from service.models import Book,Service
from datetime import datetime,timedelta,date as date2
from django.contrib import messages

from django.db.models import F, Q, When
from cart.cart import Cart
# Create your views here.
def showCart(request):   
    cart=Cart(request)
    items=cart.getItems()
    for item in items:
        #print(item.service_id)
        #print("item in item")
        #print(item['service_id'])
        serv=Service.objects.get(pk=item['service_id'])
        item['service']=serv
    context={'items':items,'auth':request.user.is_authenticated}
    #print("printing items")
    #print(items)
    total=cart.getSubtotal()
    context['total']=total
    return render(request,"cartlist.html",context)



def remove(request):
    cart=Cart(request) 
    token=request.POST['key'] 
    cart.remove(token) 
    
    return JsonResponse({'success':1})
def check(hrl,minl,hr,min):
     if(hrl<hr):
         return False
     if(hrl==hr and minl<min):
         return False
     return True
def bookpre(request):
    if(not request.user.is_authenticated):
         request.session['redirect']=reverse("cart:book-cart")
         return redirect(reverse("customer:customer-login"))
    cart=Cart(request)
    items=cart.getItems()  
    if(len(items)<1):
         return redirect(reverse('cart:cart'))
    n1=datetime.now()+timedelta(minutes=gap)
    n1=str(n1)
    hr=n1[11:13]
    min=n1[14:16]
    for item in items:
         date=item['date']
         print(date)
         slot=item['slot']
         #print(datetime.date.today())
         slarr=slot.split(":")
         hrl=slarr[0]
         minl=slarr[1]
         key=item['key']
         #date2.
         
         if(date2.fromisoformat(date)<date2.today()):
            continue
         if(date==date2.today() and not check(hrl,minl,hr,min)):
             continue
         '''' for going for payment gateway methods'''
def book(request):
     #List msgs=[]
     gap=45
     if(not request.user.is_authenticated):
         request.session['redirect']=reverse("cart:book-cart")
         return redirect(reverse("customer:customer-login"))
     if(not request.session['payment_method']):
         pass
     cart=Cart(request)
     items=cart.getItems()  
     if(len(items)<1):
         return redirect(reverse('cart:cart'))

     n1=datetime.now()+timedelta(minutes=gap)
     n1=str(n1)
     hr=n1[11:13]
     min=n1[14:16]
     for item in items:
         date=item['date']
         print(date)
         slot=item['slot']
         #print(datetime.date.today())
         slarr=slot.split(":")
         hrl=slarr[0]
         minl=slarr[1]
         key=item['key']
         #date2.
         
         if(date2.fromisoformat(date)<date2.today()):
            continue
         if(date==date2.today() and not check(hrl,minl,hr,min)):
             continue
                   
         status='UN'
         bs= Book()
         bs.dated=date
         bs.slot=slot
         bs.status=status
         bs.service=Service.objects.get(pk=item['service_id'])
         
         
        
         bs.user=request.user
         try:
          bs.save()
          messages.add_message(request,messages.INFO,'Saved your appointemet {0} {1}'.format(date,slot))
          cart.remove(key)
         except Exception as e:
           #msgs.append('Error in saving %s',date,slot)
           messages.add_message(request,messages.ERROR,'Error in saving {0} {1}'.format(date,slot))
     return render(request,'saved.html')

          

      