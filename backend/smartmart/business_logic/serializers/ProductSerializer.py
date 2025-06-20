from business_logic.models.Product import Product
from rest_framework import serializers

from business_logic.models.Category import Category


class ProductSerializer(serializers.ModelSerializer):
   category_name = serializers.CharField(source='category.name', read_only=True)
   
    # For updates (write-only)
   category  = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        write_only=True
    )
   class Meta:
       model = Product
       fields = ['id', 'name','slug', 'description','category', 'category_name',  'price', 'stock_quantity']
       read_only_fields = ['id','created_at', 'updated_at']

   