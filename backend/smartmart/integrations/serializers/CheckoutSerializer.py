from rest_framework import serializers
from integrations.models.Order import Order, OrderItem
from business_logic.models.User import AppUser
from business_logic.models.Product import Product


class OrderItemAfterConfirmationSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['order','product_id', 'quantity',"price"]
        


class OrderItemSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("Quantity must be at least 1.")
        return value
    
    
    def validate(self, data):
      try:
          product = Product.objects.get(id=data['product_id'])
      except Product.DoesNotExist:
          raise serializers.ValidationError({'product_id': 'Product does not exist'})

      if product.price != data['price']:
          raise serializers.ValidationError({'price': 'Incorrect price for the product'})

      return data
    

class CheckoutSerializer(serializers.Serializer):
    items = OrderItemSerializer(many=True)
    
  


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=AppUser.objects.all())

    #items = OrderItemSerializer(many=True)
    
    class Meta:
        model = Order
        fields = ['invoice_id','firstName', 'lastName', 'subTotal', 'tax', 'tax_ico','total', 
                 'isPaid', 'user', 'createdAt', 'updatedAt']
        #read_only_fields = ['id', 'createdAt', 'updatedAt']
    

    

    

        
