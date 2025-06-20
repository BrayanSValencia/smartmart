# myapp/models/product.py
from django.db import models
from django.utils import timezone
from .Category import Category  
from django.utils.text import slugify

class Product(models.Model):
    # Core Fields
    name = models.CharField(max_length=255, unique=True)
    slug = models.CharField(max_length=255, unique=True, editable=False)

    description = models.TextField(blank=True, null=True)  # Added per request
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField(default=0)

    # Status & Metadata
    is_active = models.BooleanField(default=True)  # Added per request
    created_at = models.DateTimeField(default=timezone.now)  # Added per request
    updated_at = models.DateTimeField(auto_now=True)  # Auto-updates on save

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
    class Meta:
        db_table = 'Product'


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image_url = models.URLField()  # Only the URL is strictly needed

    class Meta:
        db_table = 'ProductImage'