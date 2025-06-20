# Django imports
from django.http import Http404
from django.shortcuts import get_object_or_404

# Third-party imports
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView
)
from rest_framework.permissions import DjangoModelPermissions

#from knox.auth import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication


# Local imports
from business_logic.models.Product import Product
from business_logic.models.Category import Category
from business_logic.serializers.ProductSerializer import ProductSerializer
from business_logic.serializers.CategorySeriaIizer import NameCategorySerializer

class CreateProductView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,DjangoModelPermissions]
    
    queryset = Product.objects.all()

    serializer_class = ProductSerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)




class ListProductsView(ListAPIView):
    """
    List all active products
    """
    authentication_classes = []
    permission_classes = []
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer

class ProductsCategoriesView(ListAPIView):
    """
    List all active product categories
    """
    authentication_classes = []
    permission_classes = []
    serializer_class = NameCategorySerializer

    def get_queryset(self):
        return Category.objects.filter(is_active=True).only("name", "slug")
    
class ProductsCategoryView(ListAPIView):
    """
    List all active products for a given category slug
    """
    authentication_classes = []
    permission_classes = []
    serializer_class = ProductSerializer

    def get_queryset(self):
        slug = self.kwargs.get("slug")
        return Product.objects.filter(category__slug=slug, is_active=True)
    
    

class RetrieveProductView(RetrieveAPIView):
    """
    Retrieve a product by its slug
    """
    authentication_classes = []
    permission_classes = []
    serializer_class = ProductSerializer
    lookup_field = "slug"
    queryset = Product.objects.all()
    
    def get_object(self):
        try:
            return super().get_object()
        except Http404:  # Catch Django's Http404, not DRF's NotFound
            raise NotFound(detail="Sorry, we couldn't find that product. Please try again.")
    

class UpdateProductView(UpdateAPIView):
    """
    Update a product totallt or partially by slug and pk
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    def get_object(self):
        pk = self.kwargs.get("pk")
        slug = self.kwargs.get("slug")
        try:
            return Product.objects.get(pk=pk, slug=slug)
        except Product.DoesNotExist:
            raise NotFound(detail="Product not found.")

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True  # enable partial updates
        
        return super().update(request, *args, **kwargs)


class DeleteProductView(DestroyAPIView):
    """
    Delete a product by slug and pk
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,DjangoModelPermissions]
    serializer_class = ProductSerializer  
    queryset = Product.objects.all()
    def get_object(self):
        pk = self.kwargs.get("pk")
        slug = self.kwargs.get("slug")
        return get_object_or_404(Product, pk=pk,slug=slug)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Product deleted successfully"}, status=status.HTTP_200_OK)
    
class DeactivateProductView(UpdateAPIView):
    """
    Deactivate product
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,DjangoModelPermissions]
    queryset = Product.objects.all()


    def get_object(self):
        pk = self.kwargs.get("pk")
        slug = self.kwargs.get("slug")
        return Product.objects.get(pk=pk,slug=slug)

    def update(self, request, *args, **kwargs):
        product = self.get_object()
        product.is_active = False  #Deactivate product
        product.save()
        return Response({"detail": "Product deactivated successfully."})
    
    
class ActivateProductView(UpdateAPIView):
    """
    Activate product
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,DjangoModelPermissions]
    queryset = Product.objects.all()

    def get_object(self):
        pk = self.kwargs.get("pk")
        slug = self.kwargs.get("slug")
        return Product.objects.get(pk=pk,slug=slug)

    def update(self, request, *args, **kwargs):
        product = self.get_object()
        product.is_active = True  #Activate product
        product.save()
        return Response({"detail": "Product activated successfully."})