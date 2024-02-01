from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=200,null=True)
    email = models.CharField(max_length=200,null=True)

    def __str__(self):
        return str(self.name)


class Product(models.Model):
    name = models.CharField(max_length=200,null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    digital = models.BooleanField(default=False,null=True,blank=True)
    image = models.ImageField(null=True,blank=True)
    def __str__(self):
        return str(self.name)
    @property
    def imageURL(self):
        try:
            url=self.image.url
        except:
            url=''
        return url

class ProductDetail(models.Model):
    product = models.OneToOneField(Product,on_delete=models.CASCADE, null=True,blank=True)
    tag = models.CharField(max_length=200,null=True, blank=True)
    model = models.CharField(max_length=200,null=True, blank=True)
    color = models.CharField(max_length=100,null=True, blank=True)
    description = models.CharField(max_length=500,null=True, blank=True)
    image1 = models.ImageField(null=True, blank=True)
    image2 = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.product.name

    @property       
    def imageURL1(self):
        try:
            url = self.image1.url
        except:
            url = ''
        return url

    @property       
    def imageURL2(self):
        try:
            url = self.image2.url
        except:
            url = ''
        return url

class Order(models.Model):
    STATUS=(
        ('Pending','Pending'),
        ('Out for delivery','Out for delivery'),
        ('Delivered','Delivered'),
        )
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_order = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)
    status=models.CharField(max_length=200 ,null=True, choices=STATUS)

    def __str__(self):
        return str(self.id)
    @property
    def shipping(self):
        shipping = False
        orderitems =self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total 

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total 

class OrderItem(models.Model): 
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True,blank=True)
    order=models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    quantity=models.IntegerField(default=True,null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
    

class ShippingAddress(models.Model):
    Customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True,null=True)
    Order = models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    address = models.CharField(max_length=200,null=True)
    city = models.CharField(max_length=200,null=True)
    state = models.CharField(max_length=200,null=True)
    zipcode = models.CharField(max_length=200,null=True)
    
    def __str__(self):
        return str(self.address)


# Create your models here.
