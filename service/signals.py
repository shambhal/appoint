from django.db.models.signals import post_save
from django.dispatch import receiver
from  orders.models import Order,OrderItems,OrderHistory
from service.models import Book
import logging
logger = logging.getLogger(__name__)
@receiver(post_save, sender=Order)
def order_updated(sender, instance, created, **kwargs):
     print("signal processed")
     print(created)
     logger.warning(instance.status)
     logger.warning(kwargs)
     order_id=instance.id
     order=Order.objects.get(pk=order_id)
     if(order):
          items=OrderItems.objects.filter(order_id=order)
          #bh=BookHistory.objects.all.filter(order_id=order_id,status=instance.status).get()
          for item in items:
           
         
           '''''''''adding booking'''
           bo=Book.objects.all().filter(order_item_id=item.id)
           if(not bo.exists() and (order.status=='PROCESSING' )):
            bo2=Book(slot=item.slot,dated=item.dated,service=item.service)
            bo2.order_item_id=item.id
            bo2.desc=item.name
            bo2.order_id=instance.id
            bo2.name=order.name
            bo2.phone=order.name
            bo2.email=order.email
            bo2.device_id=order.device_id
            bo2.status=instance.status
            bo2.save()
     oh=OrderHistory.objects.filter(order=order).last() 
     if oh is None:
        oh=OrderHistory(order=order,status=instance.status)   
        oh.save()
     else:
        if oh.status  != instance.status :  
           oh=OrderHistory(order=order,status=instance.status)   
           oh.save() 
              
          
              
