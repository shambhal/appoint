from django.http.response import HttpResponse
from api.serializers import ServiceSerializer

from  service.models import Service


def schedule(request,*args,**kwargs) :
         
          print(request)
          return HttpResponse.write("HELLO")
          d1 = datetime(2022,5,9,15,20,15)
      
