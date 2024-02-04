from rest_framework import serializers
from service.models import Service,Book
from payment.models import Payment
from cart.models import AppCart
from orders.models import Order
class ServiceSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Service
        fields = ["name","id","sunday","monday","tuesday","thursday","friday","saturday","off",'slot']
class PaymentMethodSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Payment
        fields = ["title","status",'code']   
class CartSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = AppCart
        fields = ["slot",'dated','id']   
class RegisterSerializer(serializers.Serializer):  
       name=serializers.CharField(required=True) 
       email=serializers.CharField(required=True)
       phone=serializers.CharField(required=True,max_length=10) 
class LoginSerializer(serializers.Serializer):  
       password=serializers.CharField(required=True) 
       email=serializers.CharField(required=True)
class OrderSerializer(serializers.Serializer)  :
       
    class Meta:
        model = Order
        fields='__all__'

class ASerializer(serializers.ModelSerializer)  :
       
    class Meta:
        model = Book
        #ordering=['-id']
        fields='__all__'
        #fields=['id','dated']         
