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

from business_logic.models.Category import Category
from business_logic.serializers.CategorySeriaIizer import CategorySerializer
from business_logic.models.Product import Product

class CreateCategoryView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,DjangoModelPermissions]
    
    queryset = Category.objects.all()

    serializer_class = CategorySerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ListCategoriesView(ListAPIView):
    """
    List all categories, even if they are inactive
    """
    authentication_classes = []
    permission_classes = []
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    
class RetrieveCategoryView(RetrieveAPIView):
    """
    Retrieve a category by its slug
    """
    authentication_classes = []
    permission_classes = []
    serializer_class = CategorySerializer
    lookup_field = "slug"
    queryset = Category.objects.all()
    
    def get_object(self):
        try:
            return super().get_object()
        except Http404:  # Catch Django's Http404, not DRF's NotFound
            raise NotFound(detail="Sorry, we couldn't find that Category. Please try again.")
    

class UpdateCategoryView(UpdateAPIView):
    """
    Update a category partially by slug and pk
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def get_object(self):
        pk = self.kwargs.get("pk")
        slug = self.kwargs.get("slug")
        try:
            return Category.objects.get(pk=pk, slug=slug)
        except Category.DoesNotExist:
            raise NotFound(detail="Category not found.")

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True  # enable partial updates
        
        return super().update(request, *args, **kwargs)


class DeleteCategoryView(DestroyAPIView):
    """
    Delete a category by slug and pk
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,DjangoModelPermissions]
    serializer_class = CategorySerializer  # Not required but good to keep for consistency
    queryset = Category.objects.all()

    def get_object(self):
        pk = self.kwargs.get("pk")
        slug = self.kwargs.get("slug")
        return get_object_or_404(Category, pk=pk,slug=slug)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Category deleted successfully"}, status=status.HTTP_200_OK)
    
class DeactivateCategoryView(UpdateAPIView):
    """
    Deactivate category and all its products
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,DjangoModelPermissions]
    queryset = Category.objects.all()

    def get_object(self):
        pk = self.kwargs.get("pk")
        slug = self.kwargs.get("slug")
        return Category.objects.get(pk=pk,slug=slug)

    def update(self, request, *args, **kwargs):
        category = self.get_object()
        category.is_active = False  #Deactivate product
        category.save()
        Product.objects.filter(category=category.id).update(is_active=False)

        return Response({"detail": "The category and all its product have been deactivated successfully."})
    
    
class ActivateCategoryView(UpdateAPIView):
    """
    Activate category and all its product
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,DjangoModelPermissions]
    queryset = Category.objects.all()

    def get_object(self):
        pk = self.kwargs.get("pk")
        slug = self.kwargs.get("slug")
        return Category.objects.get(pk=pk,slug=slug)

    def update(self, request, *args, **kwargs):
        category = self.get_object()
        category.is_active = True  #Activate product
        category.save()
        Product.objects.filter(category=category.id).update(is_active=True)

        return Response({"detail": "The category and all its product have been Activated successfully."})