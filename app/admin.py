from django.contrib import admin
from .models import Profile, Product, Cart, Order, OrderItem, Payment

# Register your models here.
admin.site.register(Profile)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Payment)
