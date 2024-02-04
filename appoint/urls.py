"""pycom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
#from customer
from api.views import ServiceAPIView

#from rest_framework import routers
#from api.views import ServiceViewSet
#router = routers.DefaultRouter()
#router.register(r'api/services',ServiceViewSet )
urlpatterns = [
    path('admin/', admin.site.urls),
    
    #path('summernote/', include('django_summernote.urls')),
    
    #path("api/services/",ServiceAPIView.as_view()),
    path("api/",include("api.urls")),
    path("checkout/",include("checkout.urls",namespace="checkout")),
    #path("api/schedule/<int:service_id>/<string:date>/",include()),
    path("service/",include("service.urls",namespace="service")),
    path("mytest/",include("mytest.urls",namespace="mytest")),
    path("cart/",include("cart.urls",namespace="cart")),
     path("payment/",include("payment.urls",namespace="payment")),
    path("customer/",include("customer.urls",namespace="customer")),
    #path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='main/password/password_reset_done.html'), name='password_reset_done'),
    #path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="main/password/password_reset_confirm.html"), name='password_reset_confirm'),
    #path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='main/password/password_reset_complete.html'), name='password_reset_complete'),  
    #path("filemanager/",include("fm.urls")),
    
    path('accounts/', include('django.contrib.auth.urls')),
    path("", include("catalog.urls")),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
