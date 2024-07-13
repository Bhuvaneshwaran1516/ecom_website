from django.contrib import admin
from e_com_app.models import Category,Product,Cart,CartItem,Order,OrderItem,Favorite,ShippingAddress

# Register your models here.

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Favorite)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)