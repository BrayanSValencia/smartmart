from django.db import models

from business_logic.models.User import AppUser

class Order(models.Model):
    #id = models.CharField(max_length=24, primary_key=True)
    invoice_id = models.CharField(max_length=50, unique=True)
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    subTotal = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2)
    tax_ico = models.DecimalField(max_digits=10, decimal_places=2)

    total = models.DecimalField(max_digits=10, decimal_places=2)
    isPaid = models.BooleanField(default=True)
    user = models.ForeignKey(AppUser, on_delete=models.PROTECT, null=False)

    createdAt = models.DateTimeField()
    updatedAt = models.DateTimeField()
    
    class Meta:
        db_table = 'Order'
        
 
        
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product_id = models.CharField(max_length=24)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'OrderItem'