import os
import django
from django.core.management.base import BaseCommand
#from django.utils import timezone
from datetime import datetime

#from integrations.models import(
 #   ChatSession,
  #  ChatMessage
   # )

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartmart.settings')
django.setup()

from business_logic.models import (
    AppUser,
    Category,
    Product,
    ProductImage
    
    
)
class Command(BaseCommand):
    help = 'Populates the database with initial data'

    def handle(self, *args, **options):
        self.stdout.write("Populating database...")
        
        # Create Categories
        categories = [
            {'id': 1, 'name': 'Dairy Products', 'is_active': True},
            {'id': 2, 'name': 'Beverages', 'is_active': True},
            {'id': 3, 'name': 'Household Items', 'is_active': True},
            {'id': 4, 'name': 'Tech Products', 'is_active': True},
            {'id': 5, 'name': 'Fruit', 'is_active': True},
            {'id': 6, 'name': 'Vegetable', 'is_active': True},
        ]
        
        for cat_data in categories:
            Category.objects.update_or_create(id=cat_data['id'], defaults=cat_data)
        
        self.stdout.write("Created categories...")
        """
        # Create Users
        users = [
            {'id': 1, 'email': 'john.doe@example.com', 'username': 'john.doe', 'first_name': 'John', 'last_name': 'Doe', 'phone': '123-456-7890', 'date_of_birth': datetime(1990, 5, 15).date(), 'is_active': True},
            {'id': 2, 'email': 'jane.smith@example.com', 'username': 'jane.smith', 'first_name': 'Jane', 'last_name': 'Smith', 'phone': '987-654-3210', 'date_of_birth': datetime(1985, 8, 22).date(), 'is_active': True},
            {'id': 3, 'email': 'alice.johnson@example.com', 'username': 'alice.johnson', 'first_name': 'Alice', 'last_name': 'Johnson', 'phone': '555-123-4567', 'date_of_birth': datetime(1995, 3, 10).date(), 'is_active': True},
        ]
        
        for user_data in users:
            user, created = AppUser.objects.update_or_create(
                id=user_data['id'],
                defaults={
                    'email': user_data['email'],
                    'username': user_data['username'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                    'phone': user_data['phone'],
                    'date_of_birth': user_data['date_of_birth'],
                    'is_active': user_data['is_active'],
                }
            )
            # Set password (use this password as default for all users inserted here)
            user.set_password('Lev@1234')
            user.save()
        """
            
        
        #self.stdout.write("Created users...")
        
        # Create Products
        products = [
            # Dairy Products
            {'id': 1, 'name': 'Organic Whole Milk', 'description': 'Fresh organic whole milk.', 'category_id': 1, 'price': 4.99, 'stock_quantity': 100, 'is_active': True},
            {'id': 2, 'name': 'Greek Yogurt', 'description': 'Creamy Greek yogurt.', 'category_id': 1, 'price': 5.49, 'stock_quantity': 80, 'is_active': True},
            {'id': 3, 'name': 'Cheddar Cheese', 'description': 'Sharp cheddar cheese.', 'category_id': 1, 'price': 6.99, 'stock_quantity': 60, 'is_active': True},
            {'id': 4, 'name': 'Butter', 'description': 'Creamy unsalted butter.', 'category_id': 1, 'price': 3.99, 'stock_quantity': 90, 'is_active': True},
            # Beverages
            {'id': 5, 'name': 'Orange Juice', 'description': 'Freshly squeezed orange juice.', 'category_id': 2, 'price': 3.99, 'stock_quantity': 120, 'is_active': True},
            {'id': 6, 'name': 'Coffee Beans', 'description': 'Premium roasted coffee beans.', 'category_id': 2, 'price': 12.99, 'stock_quantity': 50, 'is_active': True},
            {'id': 7, 'name': 'Green Tea', 'description': 'Pure green tea leaves.', 'category_id': 2, 'price': 8.99, 'stock_quantity': 70, 'is_active': True},
            {'id': 8, 'name': 'Sparkling Water', 'description': 'Refreshing sparkling water.', 'category_id': 2, 'price': 2.99, 'stock_quantity': 150, 'is_active': True},
            # Household Items
            {'id': 9, 'name': 'Dish Soap', 'description': 'Effective dish soap for cleaning.', 'category_id': 3, 'price': 4.49, 'stock_quantity': 100, 'is_active': True},
            {'id': 10, 'name': 'Laundry Detergent', 'description': 'Powerful laundry detergent.', 'category_id': 3, 'price': 11.99, 'stock_quantity': 60, 'is_active': True},
            {'id': 11, 'name': 'Paper Towels', 'description': 'Absorbent paper towels.', 'category_id': 3, 'price': 7.99, 'stock_quantity': 80, 'is_active': True},
            {'id': 12, 'name': 'Toilet Paper', 'description': 'Soft and strong toilet paper.', 'category_id': 3, 'price': 9.99, 'stock_quantity': 90, 'is_active': True},
            # Tech Products
            {'id': 13, 'name': 'Smart Speaker', 'description': 'Voice-activated smart speaker.', 'category_id': 4, 'price': 99.99, 'stock_quantity': 30, 'is_active': True},
            {'id': 14, 'name': 'Wireless Earbuds', 'description': 'High-quality wireless earbuds.', 'category_id': 4, 'price': 149.99, 'stock_quantity': 40, 'is_active': True},
            {'id': 15, 'name': 'Smart Watch', 'description': 'Advanced smart watch with fitness tracking.', 'category_id': 4, 'price': 299.99, 'stock_quantity': 20, 'is_active': True},
            {'id': 16, 'name': 'Phone Charger', 'description': 'Fast-charging phone charger.', 'category_id': 4, 'price': 24.99, 'stock_quantity': 100, 'is_active': True},
            # Fruits
            {'id': 17, 'name': 'Organic Bananas', 'description': 'Fresh organic bananas.', 'category_id': 5, 'price': 2.99, 'stock_quantity': 200, 'is_active': True},
            {'id': 18, 'name': 'Fresh Strawberries', 'description': 'Sweet fresh strawberries.', 'category_id': 5, 'price': 4.99, 'stock_quantity': 150, 'is_active': True},
            {'id': 19, 'name': 'Avocados', 'description': 'Ripe avocados.', 'category_id': 5, 'price': 3.49, 'stock_quantity': 120, 'is_active': True},
            {'id': 20, 'name': 'Organic Apples', 'description': 'Crisp organic apples.', 'category_id': 5, 'price': 1.99, 'stock_quantity': 180, 'is_active': True},
            # Vegetables
            {'id': 21, 'name': 'Fresh Tomatoes', 'description': 'Juicy fresh tomatoes.', 'category_id': 6, 'price': 2.49, 'stock_quantity': 200, 'is_active': True},
            {'id': 22, 'name': 'Organic Carrots', 'description': 'Fresh organic carrots.', 'category_id': 6, 'price': 1.79, 'stock_quantity': 220, 'is_active': True},
            {'id': 23, 'name': 'Bell Peppers', 'description': 'Colorful bell peppers.', 'category_id': 6, 'price': 2.29, 'stock_quantity': 150, 'is_active': True},
            {'id': 24, 'name': 'Fresh Broccoli', 'description': 'Fresh green broccoli.', 'category_id': 6, 'price': 1.99, 'stock_quantity': 170, 'is_active': True},
        ]
        
        for prod_data in products:
            category = Category.objects.get(id=prod_data['category_id'])
            del prod_data['category_id']
            
            Product.objects.update_or_create(
                id=prod_data['id'],
                defaults={
                    **prod_data,
                    'category': category
                }
            )
        
        self.stdout.write("Created products...")
        
        # Create Product Images
        product_images = [
            {'id': 1, 'product_id': 1, 'image_url': 'https://images.pexels.com/photos/4958139/pexels-photo-4958139.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1'},
            {'id': 2, 'product_id': 2, 'image_url': 'https://images.pexels.com/photos/414262/pexels-photo-414262.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1'},
            {'id': 3, 'product_id': 3, 'image_url': 'https://images.pexels.com/photos/8531379/pexels-photo-8531379.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1'},
            {'id': 4, 'product_id': 4, 'image_url': 'https://media.istockphoto.com/id/1935462348/photo/butter-close-up.jpg?s=1024x1024&w=is&k=20&c=5j5Hsu47GtZsahb3lsqd_Ke31uWWrRkLrOzoycWJCvQ='},
            {'id': 5, 'product_id': 5, 'image_url': 'https://images.pexels.com/photos/3676/girl-morning-breakfast-orange-juice.jpg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1'},
            {'id': 6, 'product_id': 6, 'image_url': 'https://images.pexels.com/photos/27993241/pexels-photo-27993241/free-photo-of-coffee-beans-are-scattered-on-top-of-a-newspaper.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1'},
            {'id': 7, 'product_id': 7, 'image_url': 'https://images.pexels.com/photos/1581484/pexels-photo-1581484.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1'},
            {'id': 8, 'product_id': 8, 'image_url': 'https://images.pexels.com/photos/416528/pexels-photo-416528.jpeg'},
            {'id': 9, 'product_id': 9, 'image_url': 'https://images.pexels.com/photos/10574059/pexels-photo-10574059.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1'},
            {'id': 10, 'product_id': 10, 'image_url': 'https://images.pexels.com/photos/5217889/pexels-photo-5217889.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1'},
            {'id': 11, 'product_id': 11, 'image_url': 'https://images.pexels.com/photos/3941873/pexels-photo-3941873.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1'},
            {'id': 12, 'product_id': 12, 'image_url': 'https://images.pexels.com/photos/3958193/pexels-photo-3958193.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1'},
            {'id': 13, 'product_id': 13, 'image_url': 'https://images.pexels.com/photos/1279365/pexels-photo-1279365.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1'},
            {'id': 14, 'product_id': 14, 'image_url': 'https://images.pexels.com/photos/3568520/pexels-photo-3568520.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1'},
            {'id': 15, 'product_id': 15, 'image_url': 'https://images.pexels.com/photos/437037/pexels-photo-437037.jpeg'},
            {'id': 16, 'product_id': 16, 'image_url': 'https://images.pexels.com/photos/5208825/pexels-photo-5208825.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1'},
            {'id': 17, 'product_id': 17, 'image_url': 'https://images.pexels.com/photos/5945880/pexels-photo-5945880.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1'},
            {'id': 18, 'product_id': 18, 'image_url': 'https://images.pexels.com/photos/32301367/pexels-photo-32301367/free-photo-of-fresh-red-strawberries-in-water-close-up.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1'},
            {'id': 19, 'product_id': 19, 'image_url': 'https://images.pexels.com/photos/557659/pexels-photo-557659.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1'},
            {'id': 20, 'product_id': 20, 'image_url': 'https://images.pexels.com/photos/1870725/pexels-photo-1870725.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1'},
            {'id': 21, 'product_id': 21, 'image_url': 'https://images.pexels.com/photos/32301556/pexels-photo-32301556/free-photo-of-close-up-of-fresh-ripe-red-tomatoes-on-vine.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1'},
            {'id': 22, 'product_id': 22, 'image_url': 'https://images.pexels.com/photos/3650647/pexels-photo-3650647.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1'},
            {'id': 23, 'product_id': 23, 'image_url': 'https://images.pexels.com/photos/1274670/pexels-photo-1274670.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1'},
            {'id': 24, 'product_id': 24, 'image_url': 'https://images.pexels.com/photos/32301529/pexels-photo-32301529/free-photo-of-fresh-broccoli-plant-in-outdoor-garden-setting.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1'},
        ]
        
        for img_data in product_images:
            product = Product.objects.get(id=img_data['product_id'])
            del img_data['product_id']
            
            ProductImage.objects.update_or_create(
                id=img_data['id'],
                defaults={
                    **img_data,
                    'product': product
                }
            )
        
        self.stdout.write("Created product images...")
        

        self.stdout.write(self.style.SUCCESS("Successfully populated database!"))
        
if __name__ == '__main__':
    Command().handle()