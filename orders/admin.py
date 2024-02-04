from django.contrib import admin
from .models import Order
from config.helper import formatPrice
class OrderAdmin(admin.ModelAdmin) :
  
   
 list_display=['id','Total','Customer']
 def Total(self,obj):
    return formatPrice(obj.total)
 def Customer(self,obj):
    return obj.name +' - '+obj.phone
 def od(sel,obj):
   ####order details
   pass
admin.site.register(Order,OrderAdmin)

