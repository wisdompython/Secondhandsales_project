from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200,null=True, blank=True)#

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200, unique=True)
    image=models.ImageField(default='default.jpg')
    description = models.CharField(max_length=500)
    features = models.TextField(null=True, blank=True)
    category = models.ManyToManyField(Category, blank=True)
    reason_for_sale = models.TextField(null=True, blank=True)
    usage_duration = models.TextField(null=True, blank=True)
    size = models.CharField(max_length=200,null=True, blank=True)
    condition = models.CharField(max_length=200,null=True, blank=True)
    price = models.FloatField()
    seller = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    is_digital = models.BooleanField(default=False)
    def __str__(self):
        return self.name

class Comment(models.Model):
    commentproduct = models.ForeignKey(Product, on_delete=models.CASCADE)
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.body

    
class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    completed = models.BooleanField(default=False)
    order_date = models.DateTimeField(default=timezone.now)
    transaction_id = models.CharField(max_length=200, null=True)

    @property # get total amount to be spent
    def get_grand_total(self):
        items = self.orderitem_set.all()
        for i in items:
            if i.agreed_price:
                i.product.price = i.agreed_price
            total = sum([i.get_total for i in items])
        total = sum([total.get_total for total in items])
        return total
    @property
    def get_cart_total(self): # get total no of items in the cart
        items = self.orderitem_set.all()
        total = sum([total.quantity for total in items])
        return total
    
    @property
    def ship(self):
        shipping = False
        item = self.orderitem_set.all()
        for i in item:
            if i.product.is_digital == False:
                shipping = True
        return shipping
    

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField(default=1)
    order = models.ForeignKey(Order,on_delete=models.CASCADE, null=True, blank=True)
    agreed_price = models.IntegerField(blank=True, null=True)

    # function to return total amount 
    def __str__(self):
        return self.product.name
    @property
    def get_total(self):
        if self.agreed_price:
            total = self.quantity * self.agreed_price
        total = self.quantity * self.product.price
        return total
    @property
    def get_new_total(self):
        total = self.quantity * self.agreed_price
        return total
   
       
    
class ShippingAddress(models.Model):
    customer = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    order = models.ForeignKey(Order,on_delete=models.CASCADE,null=True)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=200)

class Negotiation(models.Model):
    order_item = models.ForeignKey(OrderItem,on_delete=models.CASCADE,null=True,blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    sent_to = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True, related_name='sent_to')
    body = models.TextField()
    completed = models.BooleanField(default=False)
    
class QA(models.Model): #  question and answer model
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True,blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    body = models.TextField()
