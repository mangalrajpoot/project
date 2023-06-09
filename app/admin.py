from django.contrib import admin
from .models import *

# Register your models here.

class CustomerAdmin(admin.ModelAdmin):
    list_display=['user','name','locality','city','state','zipcode']

class ProductAdmin(admin.ModelAdmin):
    list_display=['title','discounted_price','selling_price','description','brand','category','product_image']
    list_display_links=['brand']

class CartAdmin(admin.ModelAdmin):
    list_display=['user','product','quantity']

class OrderPlacedAdmin(admin.ModelAdmin):
    list_display=['user','customer','product','quantity','ordered_date','status']

admin.site.register(Customer,CustomerAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Cart,CartAdmin)
admin.site.register(OrderPlaced,OrderPlacedAdmin)