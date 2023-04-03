from django.contrib import admin
from .models import Category,Product,OrderItem, Order, ShippingAddress,Comment, Negotiation,QA
# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(ShippingAddress)
admin.site.register(Comment)
admin.site.register(Negotiation)
admin.site.register(QA)