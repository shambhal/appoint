from django.contrib import admin
from django.urls import path,include
from django.views.generic.edit import CreateView
from checkout import views
app_name="checkout"
urlpatterns = [
path('payment',views.payment_view,name="pview"),
path("success",views.success,name="success"),
path("fail",views.fail,name="fail"),
]