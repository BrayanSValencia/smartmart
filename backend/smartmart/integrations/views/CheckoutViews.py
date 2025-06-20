# Standard Library
import uuid
import hashlib
from decimal import Decimal, ROUND_HALF_UP

# Django
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
from django.db import transaction

# Third-party imports
from decouple import config
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework_simplejwt.authentication import JWTAuthentication


# Local Apps
from business_logic.models.Product import Product
from business_logic.models.User import AppUser
from integrations.serializers.CheckoutSerializer import (
    CheckoutSerializer,
    OrderItemAfterConfirmationSerializer,
    OrderSerializer
)
from integrations.models.Order import Order
from integrations.views.IsInGroupCheckout import IsInGroup

P_CUST_ID_CLIENTE = config('P_CUST_ID_CLIENTE', default=None)
P_KEY = config('P_KEY', default=None)


class EpaycoCheckoutView(APIView):
    """
    Return crafted ePayco payment data without calling the ePayco API.

    Input
    {
        "items": [
            {"product_id": 1, "quantity": 2, "price": 25000},
            {"product_id": 2, "quantity": 1, "price": 18000}
        ]
    }
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,IsInGroup]

    def post(self, request):
        serializer = CheckoutSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            validated_data = serializer.validated_data
            subtotal = Decimal('0')
            items_description = []

            for item in validated_data['items']:
                product = Product.objects.get(pk=item['product_id'])
                subtotal += (product.price ) * item['quantity']
                items_description.append(f"{item['quantity']}x {product.name},")

            tax = (subtotal * Decimal('0.19')).quantize(Decimal('0'), rounding=ROUND_HALF_UP)
            total = subtotal + tax

            invoice = f"INV-${uuid.uuid4()}"
            cache.set(f"{invoice}", validated_data['items'], timeout=300)  # Cache the item data temporarily for 5 minutes
            user = request.user

            # Return ONLY the crafted data (no ePayco API call)
            return Response({
                'currency': "usd",
                'amount': total,
                'tax_base': subtotal,
                'tax': tax,
                'name': "Order from Smartmart",
                'description': " | ".join(items_description),
                'invoice': invoice,
                'external': "false",
                'response': 'https://f44a-181-53-99-76.ngrok-free.app/epayco/response/',
                'confirmation': 'https://f44a-181-53-99-76.ngrok-free.app/checkoutconfirmation/',
                "x_extra1": user.username,
            })

        except Product.DoesNotExist:
            return Response(
                {'error': 'Invalid product ID'},
                status=status.HTTP_400_BAD_REQUEST
            )


class EpaycoPaymentConfirmationView(APIView):
    """
    Handles payment confirmation from ePayco
    """
    authentication_classes = []  # ePayco won't send tokens
    permission_classes = [AllowAny]

    @csrf_exempt
    def post(self, request):
        data = request.data

        # Extract required fields
        x_ref_payco = data.get("x_ref_payco")
        x_transaction_id = data.get("x_transaction_id")
        x_amount = data.get("x_amount")
        x_currency_code = data.get("x_currency_code")
        x_signature = data.get("x_signature")
        x_invoice = data.get("x_id_factura")
        x_extra1 = data.get("x_xextra1")  

        # Signature validation
        signature_string = f"{P_CUST_ID_CLIENTE}^{P_KEY}^{x_ref_payco}^{x_transaction_id}^{x_amount}^{x_currency_code}"
        calculated_signature = hashlib.sha256(signature_string.encode("utf-8")).hexdigest()

        if calculated_signature != x_signature:
            return Response({"error": "Invalid signature"}, status=status.HTTP_401_UNAUTHORIZED)

        # Get cached items
        purchased_items = cache.get(x_invoice)
        
        if not purchased_items:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


        if data.get("x_cod_transaction_state") == "1":
            try:
                user_id = AppUser.objects.filter(username=x_extra1).values_list("id", flat=True).first()
                if not user_id:
                    return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

                self.create_order(purchased_items, user_id, data)
                return Response({"message": "Payment confirmation processed"}, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"message": "Payment not accepted"}, status=status.HTTP_200_OK)

    def create_order(self, purchased_items, user_pk, data):
        if not data or not purchased_items:
            raise ValueError("Missing data or purchased items")

        invoice_id = data.get("x_id_factura")

        if Order.objects.filter(invoice_id=invoice_id).exists():
            raise ValueError("Order with this invoice already exists")

        try:
            with transaction.atomic():
                # Create the Order
                order_data = {
                    "invoice_id": invoice_id,
                    "firstName": data.get("x_customer_name", ""),
                    "lastName": data.get("x_customer_lastname", ""),
                    "subTotal": Decimal(data.get("x_amount_base", "0")),
                    "tax": Decimal(data.get("x_tax", "0")),
                    "tax_ico": Decimal(data.get("x_tax_ico", "0")),
                    "total": Decimal(data.get("x_amount", "0")),
                    "isPaid": True,
                    "user": user_pk,
                    "createdAt": data.get("x_transaction_date"),
                    "updatedAt": data.get("x_transaction_date"),
                }

                serializer = OrderSerializer(data=order_data)
                serializer.is_valid(raise_exception=True)
                order_instance = serializer.save()

                # Create OrderItems
                for item in purchased_items:
                    order_item_data = {
                        "order": order_instance.id,  
                        "product_id": item['product_id'],
                        "quantity": item['quantity'],
                        "price": Decimal(str(item['price']))
                    }
                    item_serializer = OrderItemAfterConfirmationSerializer(data=order_item_data)
                    item_serializer.is_valid(raise_exception=True)
                    item_serializer.save()

                cache.delete(invoice_id)
                return order_instance

        except Exception as e:
            print(f"Order creation failed: {str(e)}")
            raise