from django.db import models
from django.contrib.auth.models import User
import datetime
import os
from datetime import datetime, timedelta

def getFileName(request,filename):
    now_time=datetime.datetime.now().strftime("%Y%m%d%H:%M%S")
    new_filename="%s%s"%(now_time,filename)
    return os.path.join('image/uploads/',new_filename)

class Category(models.Model):
    name=models.CharField(max_length=100)
    image=models.ImageField(upload_to=getFileName)
    description=models.TextField(max_length=500)
    status=models.BooleanField(default=False,help_text="0-show,1-Hidden")
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    vendor=models.CharField(max_length=100)
    image=models.ImageField(upload_to=getFileName)
    quantity=models.IntegerField()
    original_price=models.IntegerField()
    selling_price=models.IntegerField()
    discount=models.IntegerField()
    description=models.TextField(max_length=500)
    status=models.BooleanField(default=False,help_text="0-show,1-Hidden")
    trending=models.BooleanField(default=False,help_text="0-show,1-Hidden")
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"Cart of {self.user.username}"

    @property
    def total_items(self):
        return sum(item.product_quantity for item in self.cart_items.all())

class CartItem(models.Model):
    cart=models.ForeignKey(Cart,related_name='cart_items', on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    product_quantity=models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product_quantity} X {self.product.name}"
    
    def total_price(self):
        return self.product_quantity * self.product.selling_price
    
    
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'product')

    def _str_(self):
        return f"{self.user.username} favorites {self.product.name}"
    
class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    order_date = models.DateField(auto_now_add=True,null=True)
    delivery_date = models.DateField(null=True, blank=True)  
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    def save(self, *args, **kwargs):
        if not self.delivery_date:
            # Calculate delivery date 5 days from now
            self.delivery_date = datetime.now().date() + timedelta(days=5)
        super().save(*args, **kwargs)
    def __str__(self):
        return f"Order {self.id} by {self.user.username} - Total: {self.total_price}"

   
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def _str_(self):
        return f"{self.quantity} of {self.product.name}"
   

class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    phone_number=models.BigIntegerField(null=True)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username} - {self.address_line_1}, {self.city}, {self.country}, {self.phone_number}"
