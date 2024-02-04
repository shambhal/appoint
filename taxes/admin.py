from django.contrib import admin
from .models import Tax
# Register your models here.
@admin.register(Tax)
class TaxesAdmin(admin.ModelAdmin)  :
    list_display=['name','type','status','sort_order']
    pass  