
from rest_framework import serializers

from business_logic.models.Category import Category

class NameCategorySerializer(serializers.Serializer):
    name = serializers.CharField()
    slug= serializers.CharField()
    
class CategorySerializer(serializers.ModelSerializer):
   
   class Meta:
       model = Category
       fields = ['id', 'name','slug','is_active']
       read_only_fields = ['id','created_at', 'updated_at']
