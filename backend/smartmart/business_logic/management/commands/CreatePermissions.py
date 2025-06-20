from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from business_logic.models.Product import Product
from business_logic.models.Category import Category
from business_logic.models.User import AppUser


class Command(BaseCommand):
    help = "Create roles (groups) and assign model permissions"

    def handle(self, *args, **options):
        # Create or get groups
        
        staff_group, _ = Group.objects.get_or_create(name="Staff")
        user_group, _ = Group.objects.get_or_create(name="User")

        # Get content types
        product_ct = ContentType.objects.get_for_model(Product)
        category_ct = ContentType.objects.get_for_model(Category)
        user_ct= ContentType.objects.get_for_model(AppUser)


        # Permissions for User
        user_add = Permission.objects.get(codename='add_appuser', content_type=user_ct)
        user_view = Permission.objects.get(codename='view_appuser', content_type=user_ct)
        user_change = Permission.objects.get(codename='change_appuser', content_type=user_ct)
        user_delete = Permission.objects.get(codename='delete_appuser', content_type=user_ct)
        
        # Permissions for Product
        product_add = Permission.objects.get(codename='add_product', content_type=product_ct)
        product_view = Permission.objects.get(codename='view_product', content_type=product_ct)
        product_change = Permission.objects.get(codename='change_product', content_type=product_ct)
        product_delete = Permission.objects.get(codename='delete_product', content_type=product_ct)

        # Permissions for Category
        category_add = Permission.objects.get(codename='add_category', content_type=category_ct)
        category_view = Permission.objects.get(codename='view_category', content_type=category_ct)
        category_change = Permission.objects.get(codename='change_category', content_type=category_ct)
        category_delete = Permission.objects.get(codename='delete_category', content_type=category_ct)

 

        # Assign to Staff group 
        staff_group.permissions.set([
        
        product_add, product_view, product_change, product_delete,
        category_add, category_view, category_change, category_delete,
        ])

        # Assign to User group (view only)
        user_group.permissions.set([
            product_view,
            category_view,
            #Checkout
            
        ])

