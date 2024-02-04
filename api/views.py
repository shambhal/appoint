from django.http.response import HttpResponse
from api.serializers import ServiceSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import  viewsets
import json
import payment.urls
from django.urls import reverse
from service.helpers import generateKey
from rest_framework.decorators import api_view, renderer_classes
#from rest_framework.renderers import JSONRenderer, TemplateHTMLRendere
from django.contrib.auth.models import User
from django.db import transaction
from datetime import date
from config.helper import formatPrice
from  service.helpers import changeto24hrs ,generateKey
from rest_framework.views import APIView
from guser.models import GUser
from api.utils.dayslots import DaySlots,CartPrice,ServiceSlotPrice
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.conf import settings
import json
import datetime
from customer.models import Customer
from django.forms import model_to_dict
from service.models import SSpecial, Service,Book
from cart.models import AppCart
from  service.models import Service
import importlib
import os.path
from orders.models import Order,OrderItems,OrderTotals
from payment.models import Payment
from django.apps import apps
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import OrderSerializer,ASerializer
from .serializers import ServiceSerializer,LoginSerializer,PaymentMethodSerializer,CartSerializer,RegisterSerializer
dayarr=['monday','tuesday','wednesday','thursday','friday','saturday','sunday']

def isGOC(user):
    gu=GUser.objects.all().filter(user=user)
    if(gu.exists()):
      return 'guest'
    if(Customer.objects.all().filter(user=user)).exists():
        return 'customer'
class ServiceAPIView(APIView):
    def get(self,request,*args,**kwargs) :
     queryset = Service.objects.all()
     serializer_context = {
            'request': request,
        }
     serializer = ServiceSerializer(queryset,many=True,context=serializer_context)
     return Response(serializer.data)

     return Response(serializer.data) 
    
class DeleteCartView(APIView):
    def post(self,request,*args,**kwargs):
        cart_id=request.data['cart_id']
        device_id=request.data['device_id']
        AppCart.objects.filter(id=cart_id).delete()
        return JsonResponse({'success':1})
class RegenerateKey(APIView):
    def post(self,request,*args,**kwargs):
         token =request.data['token']
         obj=GUser.objects.filter(access=token)
         if(obj.exists()):
                obj=obj.first()
                user=User.objects.get(pk=obj.user_id)
                refresh=RefreshToken.for_user(user)
                GUser.objects.filter(pk=obj.id).delete()
                gu=GUser(user=user)
                gu.refresh=str(refresh)
                gu.access=str(refresh.access_token)
                gu.save()
                return Response({'access':gu.access,'refresh':gu.refresh,'success':1,'type':'guest'})
         obj=Customer.objects().filter(access=token)
         if(obj.exists()):
                user=User.objects.get(pk=obj.user_id)
                refresh=RefreshToken.for_user(user)
                
                objs=Customer.objects().filter(access=token)
                objs.access=refresh.access_token
                objs.refresh=str(refresh)
                objs.save()
                return Response({'access':gu.access,'refresh':gu.refresh,'success':1,'type':'customer'})
class BookView(APIView)  :
 def post(self,request,*args,**kwargs) :
      order_id= request.data['order'] 
      order=Order.objects.get(pk=order_id)
      items=OrderItems.objects.filter(order_id=order_id)
      for item in items:
          
          slot=changeto24hrs(item.slot)
          b=Book(name=order.name,phone=order.phone,email=order.email)
          b.service =Service.objects.get(pk=item.service_id) 
          b.dated=item.dated
          b.slot=str(slot[0])+':'+str(slot[1])
          b.desc=item.name
          b.status='BOOKED'
          b.order_item_id=item.id
          b.device_id=request.data['device_id'] if request.data['device_id']!=None else ''
          b.order_id=item.order_id.id
          print(b)
          b.save()
      return JsonResponse({'success':1})   
class ServiceSlotsView(APIView):
 def get(self,request,*args,**kwargs):
   ''''SLOTS DAY SERVICE'''
   sparr=[]
   rarr=[]
   barr=[]
   daily={}
   service_id=request.GET['service_id']
   if('dated' in request.GET):
          dat=request.GET['dated']
   else:
         dat=str(datetime.datetime.today()).split(" ")[0]
   '''   
   dt =datetime.datetime.strptime(dat,'%Y-%m-%d')
   wd=dt.weekday()
   serv=Service.objects.get(pk=service_id)
   if serv!=None:
       s=model_to_dict(serv)
       routine={'hours':s[dayarr[wd]],'off':serv.off}
       daily['hours']=s[dayarr[wd]]
       daily['off']=serv.off
   sps=[]  
   spstring=''
   spoff=''
   specialobj=SSpecial.objects.all().filter(service_id=service_id,sdate=dat) 
   if(specialobj.exists()):
        for rec in specialobj:
           sps.append(rec.hours)
        spstring=','.join(sps)
        spoff=rec.off
    
   bookings=[]
   obj=Book.objects.all().filter(service_id=service_id,dated=dat)
   
   if obj.exists():
            for rec in obj:
             bookings.append(rec.slot)
            
             obj2=','.join(bookings)
   else:
            obj2=''   


   
   ds=DaySlots(s['slot'],dat)
   ds.makeslots(daily['hours'],'routine')
   ds.makeslots(daily['off'],'off')
   ds.makeslots(obj2,'book')
   ds.makeslots(spstring,'special')
   sched=ds.getSchedule()
   '''
   ssp=ServiceSlotPrice()
   ssp.service_id=service_id
   ssp.dated=dat
   sched=ssp.calculateSchedule()
   return JsonResponse({'list':sched,'date':dat,'service_name':ssp.service_name})
   #return JsonResponse({'routine':routine,'sched':sched,'Sbook':obj2,'spoff':spoff,'sp':spstring,'date':dat})
class TermsAPIView(APIView):
    def get(self,request):  
        return Response({'text':'Hello you should abide to our terms and conditions.'},200) 
class PaymentMethodsAPIView(APIView):
    def get(self,request,*args,**kwargs) :
     queryset = Payment.objects.all().filter(status=1)
     serializer_context = {
            'request': request,
        }
     serializer = PaymentMethodSerializer(queryset,many=True,context=serializer_context)
     return Response(serializer.data)   
class HomeAPIView(APIView):
   def get(self,request,*args,**kwargs):
       banners=[{'name':'Medical','id':1,'img':'http://192.168.1.2:8000/static/imgs/slides/2.jpg'},
                
         {'name':'Service2','id':2,'img':'http://192.168.1.2:8000/static/imgs/slides/1.jpg'},

       ]
       ret={'banners':banners}
       return Response(ret)
class ATCView(APIView):

    def post(self,request):
         slot=request.data['slot']
         dated=request.data['dated']
         service_id=request.data['service_id']
         user=request.user
         
         
             
         service=Service.objects.get(pk=service_id*1)
         #price=request.data['price']
         ### change here for user
         #user can be anonyimous user
         
         a=AppCart(slot=slot,dated=dated,service=service)
         '''nere logic will prevent this'''
         if(user.id is None ):
             rm=AppCart.objects.filter(slot=slot,dated=dated,service=service,device_id=request.data['device_id'])
             a.device_id=request.data['device_id']
         else:
             a.user_id=user.id
             rm=AppCart.objects.filter(slot=slot,dated=dated,service=service,user_id=user.id)
         rm.delete()
         a.save()
         return Response({'success':1})

'''def init(request):
           
           if(request.user.id is None):
            key=generateKey(0)
            user = User.objects.create_user(username=key,
                                 email=key,
                                 password=key)
            gs=GUser.objects.create(user=user,key=key) 

           return Response({'success':1})
'''


@api_view(('GET',))
def init2(request):
       if( request.user.id is None):
            key=generateKey(0)
            email='guest'+key[1]+'@guestaccount.com'
            user=User.objects.create_user(username=key[0],password=key[1],email=email,first_name="guest" ,last_name="guest")
            refresh=RefreshToken.for_user(user)
            #print(len(refresh))
            #print(len(str(refresh.access_token)))
            #return Response()
            gu=GUser(user=user)
            gu.refresh=str(refresh)
            gu.access=str(refresh.access_token)
            gu.save()
            return Response({'access':gu.access,'refresh':gu.refresh,'success':1,'type':'guest'})
       return Response({'type':'customer','id':request.user.id})

'''def init(request):
    userid=11
    userobj=User.objects.get(pk=userid)
    if(userobj is None):
        return Response("user object is none")
    gu=GUser.objects.filter(user=userobj)
    if( not gu.exists()):
        return Response("user is not guest")
    else:
        return Response("user is guest")
'''        
class PMShow(APIView):
    def post(self,request,*args,**kwargs):
        order_id=request.data['order_id']
        oinfo=Order.objects.get(pk=order_id)
        if(oinfo):
            pm=oinfo['payment_method']
            if(oinfo['status']!='CREATED'):
                return Response({'error':'Order is not fresh'})
            #param="."+oinfo['payment_method']+'.hooks'   
            #mod=importlib.import_module(param, 'payment.gateways') 
            return Response({'success':1}) 
            

class PMDetailsAPIView(APIView):
    def get(self,request,*args,**kwargs) :
     name=request.GET['method']
     print("name is "+name)
     '''
     models=AppConfig.get_models('pycom')
     for m in models:
        print(m)
     '''   
     Model=apps.get_model(name.lower(),name,False)
     queryset = Model.objects.first()
     #print(queryset.email) 
     path2=os.path.join(settings.BASE_DIR,'payment/gateways/paypal/hooks')
     module=importlib.import_module('payment.gateways.paypal.hooks')
     ret=module.getQuote(request)
     #module = importlib.import_module(module_name)
     return Response(json.dumps(ret))
class AppointView(APIView)  :
    def post(self,request,*args,**kwargs)  :
         user=request.user
         #print(request.data['device_id'])
         if(not user.id is None):
              aitems=Book.objects.all().filter(user_id=user.id)  
         else:     
           aitems=Book.objects.all().filter(device_id=request.data['device_id']) 
         serializer_context = {
            'request': request,
        }
         #print(aitems)
         serializer = ASerializer(aitems,many=True)#,context=serializer_context)   
         print(serializer.data)
         return Response(serializer.data)
class AListView(APIView):
    pass    
class CartListView(APIView):
    datearr=[]
    def __getPrice(self,item):
         dated=item.dated
         slot=item.slot
         slot=slot.replace("AM",'')
         slot=slot.replace("A.M",'')
         slot=slot.replace("PM",'')
         slot=slot.replace(":",'')
         service_id=item.service_id
         ssp=ServiceSlotPrice()
         ssp.service_id=service_id
         ssp.dated=dated
         sched=ssp.calculateSchedule()
        # return sched
         for nod in sched:
             #print( nod)
             #return nod
             if(nod['key']==int(slot) and nod['av']==1):
              return nod['wprice']
         return -1   

    '''def __getTotals(self,items):
         total=0
         for item in items  :
             #pass
             total=total+float(item['price'])
         return [{'title':'total','text':str(formatPrice(total))}]      
    '''
    def get(self,request):
         ########make user id dynamic########
         user=request.user
         print(user.id)
         if(not user.id is None):
           user_id=user.id
           #customer=Customer.objects.get(pk=user_id)
           #if(not customer.DoesNotExist()):
           AppCart.objects.all().filter(user_id=user_id,dated__lt= date.today()) .delete()
           cartitems=AppCart.objects.all().filter(user_id=user_id)  
           '''else:
               guser=GUser.objects.get(pk=id)
            '''   
         else:
             '''device_id=request.data['device_id']
                AppCart.objects.all().filter(dated__lt= datetime.now) .delete()
             cartitems=AppCart.objects.all().filter(device_id=device_id)  
             '''
             cartitems=[]
         arr=[]
         print(cartitems)
         cp=CartPrice()
         for item in cartitems: 
             
             item.price=cp.getPrice(item)
             price=item.price
             #return JsonResponse({'PRICE':price})
             if(price !=-1):
              obj={'slot':item.slot,'dated':item.dated,'price':price,'fprice':formatPrice(price),'cart_id':item.id,'name':item.service.name,'quantity':1,
                  'options':[{'name':'Date :','value':str(item.dated)},{'name':'Slot','value':item.slot}]
                  }
                     
              arr.append(obj)
         subtotal=cp.getSubtotal(arr)    
         cp.calculateTotals()
         totals=cp.getTotals()
         serializer = CartSerializer(arr,many=True)
         return JsonResponse({'totals':totals,'products':arr}  )
class DetailView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request):
              user = request.user
              return JsonResponse(model_to_dict(user))
class LoginView(APIView):
   
    def post(self,request):
            
           l=LoginSerializer(data=request.data)
           if(not l.is_valid()):
                 return JsonResponse({'error':'1','msg':l.errors})
           email=request.data['email']
           password=request.data['password']  
           user = authenticate(username=email, password=password)
           if user is None:
             #print(user)
             return JsonResponse({'error':'Invalid Credentials'})  
           #try:
           refresh = RefreshToken.for_user(user)
           refresh_token = str(refresh)
           access_token = str(refresh.access_token)

            #update_last_login(None, user)

           validation = {
                'access': access_token,
                'refresh': refresh_token,
                'info':{'email': user.email,
                        'first_name':user.first_name,
                        'last_name':user.last_name,
                'customer_id':user.id}
            }

           return JsonResponse(validation)
           #except e
             #return JsonResponse({'error':1,'msg':l.errors})  

class OrderSummary(APIView):
    def post(self,request):
         orderid=request.data['order_id']
         user_id=request.user.id
         order=Order.objects.get(pk=orderid)
         if(not order is None) :
              if(order.user_id != user_id):
                  return JsonResponse({'error':'Unauthorized'})
              #device_id=request.data['device_id']
              ##if(device_id is None):
              #    return JsonResponse({'error':'Unauthenticated'})
             
              items=OrderItems.objects.filter(order_id=order)
              iarr=[]
              for item in items:
                  temp=item
                  temp.price= formatPrice(item.price) 
                  iarr.append(model_to_dict(temp))
              otarr=[]
              ots=OrderTotals.objects.filter(order_id=order)
              for o in ots:
                  tempo=o
                  tempo.total=formatPrice(o.total)
                  otarr.append(model_to_dict(tempo))

              return JsonResponse({'order':model_to_dict(order),'items':iarr,'totals':otarr,'url':request.build_absolute_uri('payment/showpay')})
class OrderView(APIView):
    def __saveTotals(self,order_id,arr):
           #arr=json.loads(arrstring)
           order=Order.objects.get(pk=order_id)
           OrderTotals.objects.filter(order_id=order).delete()
           for node in arr :
               oi=OrderTotals.objects.create(title=node['name'],order_id=order,total=node['total'])
    def __saveitems(self,order_id,arr):
           #arr=json.loads(arrstring)
           #print(arr)
           order=Order.objects.get(pk=order_id)
           OrderItems.objects.filter(order_id=order).delete()
           for node in arr:
               #node.order=order_id
               oi=OrderItems()
               oi.order_id=order
               oi.name=node['name']
               oi.slot=node['slot']
               oi.price=node['price']
               oi.dated=node['dated']
               oi.service=node['service']
               oi.save()
    def post (self,request) :
         d=request.data.copy()
         user=request.user
         if(not user.id is None):
           user_id=user.id
           goc=isGOC(user)
           #customer=Customer.objects.get(pk=user_id) 
           cartitems=AppCart.objects.all().filter(user_id=user_id)  
         else:
             device_id=request.data['device_id']
             cartitems=AppCart.objects.all().filter(device_id=device_id)  

         arr=[]
         cp=CartPrice()
         
         for item in cartitems: 
             item.price=cp.getPrice(item)
             price=item.price
             #return JsonResponse({'PRICE':price})
             if(price !=-1):
              obj={'slot':item.slot,'dated':item.dated,'price':price,'fprice':formatPrice(price),'cart_id':item.id,'name':item.service.name,'quantity':1,
                  'service':item.service,'options':[{'name':'Date :','value':str(item.dated)},{'name':'Slot','value':item.slot}]
                  }
           
              arr.append(obj)
             
         subtotal=cp.getSubtotal(arr)    
         cp.calculateTotals()
         gtotal=cp.grandtotal
         '''if(not user.id==None):
             


         user=Customer.objects.get(pk=1)
         name=user.user.first_name+ ' '+user.user.last_name
         phone=user.phone
         '''
         
         phone=request.data['phone']
         name=request.data['name']
         email=request.data['email']
         comment=request.data['comment']
        
       
         tarr={
             
         'phone':phone,
         'device_id':d['device_id'],
         'name':name,
          'user_id':request.user.id,
         'total':gtotal,
         'payment_method':d['payment_method'],
         'email':email,
         'status':'CREATED',
         'comment':comment

         }
        
         flag=True
         ords=OrderSerializer(data=tarr)
         if('order_id' in request.data):
             
             flag=False
         if(ords.is_valid()):
            if(flag==True):
             o=Order.objects.create(**tarr)
            #o.save()
             orderid=o.id
            else:
                orderid=request.data['order_id']
                o=Order.objects.filter(pk=orderid).update(**tarr)
                
            self.__saveitems(orderid,arr)
            self.__saveTotals(orderid,cp.getTotals())
            cartitems.delete()
            return JsonResponse({'success':1,'order_id':orderid})
         else:
            return  JsonResponse({'errors':ords.errors})  
class ConfirmView(APIView):
     def post(self,request):
         oid= request.data['order_id']
         ord=Order.objects.get(pk=oid)
         items=OrderItems.objects.all().filter(order_id=ord)
         iarr=[]
         for item in items:
             iarr.append(model_to_dict(item))
         #print(ord.OrderItems)
         return JsonResponse({'order':model_to_dict(ord),'items':iarr})     
class RegisterView(APIView):
    def __checkUsername(self,username):
          u=User.objects.all().filter(username=username)
          if(u.exists()):
             return False
          else:
              return True
    def post(self,request) :
         serial=RegisterSerializer(data=request.data)
         if(serial.is_valid()):
             d=request.data
             narr=request.data['name'].split(' ')
             first_name=narr[0]
             last_name=narr[1] if len(narr)>2 else ''
             username=d['email']
             email=username
             if self.__checkUsername(username)==False:
                   return JsonResponse({'error':1,'msg':'Duplicate Username'})
             '''u=User(username=username)
             u.email=email
             u.password='123456'
             u.first_name=first_name
             u.last_name=last_name
             u.is_active=True
             u.save()'''
             u=User.objects.create_user(username,email,'123456')
             u.first_name=first_name
             u.last_name=last_name
             u.save()
             c=Customer(user=u,phone=d['phone'])
             c.save()
             return Response({'success':1},200)   

                 
         else:
             return Response({'error':1,'msg':serial.errors},200)