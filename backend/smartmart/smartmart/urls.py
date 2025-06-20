# Django imports
from django.contrib import admin
from django.urls import path

# Local imports
from business_logic.views.AuthenticationView import CreateStaffUserView, LoginView, LogoutView, RegisterView, VerifyEmailView


from business_logic.views.CategoryView import(
    CreateCategoryView,
    ListCategoriesView,
    RetrieveCategoryView,
    UpdateCategoryView,
    DeleteCategoryView,
    DeactivateCategoryView,
    ActivateCategoryView
    
    
) 

from business_logic.views.ProductView import (
    CreateProductView,
    DeleteProductView,
    RetrieveProductView,
    UpdateProductView,
    ProductsCategoriesView,
    ProductsCategoryView,
    ListProductsView,
    DeactivateProductView,
    ActivateProductView
)

from business_logic.views.UserView import (
    DeleteUserView,
    RetrieveUserView,
    UpdateUserView,
    DeactivateUserAccount,
    RetrieveUserView
)

from integrations.views.CheckoutViews import (
    EpaycoCheckoutView,
    EpaycoPaymentConfirmationView,
    
)

from integrations.views.CheckoutHTML import (
    EpaycoResponseHTMLView
    
)

#third party imports

from rest_framework_simplejwt.views import (
    
    TokenRefreshView,
)

urlpatterns = [
    #Admin
    path('admin/', admin.site.urls),
    path('deleteuser/', DeleteUserView.as_view(), name='deleteuser'),
    path('createstaffuser/', CreateStaffUserView.as_view(), name='verifyemail'),

    
    #Authentication view
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('verifyemail/<str:token>/', VerifyEmailView.as_view(), name='verifyemail'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh'),

    #User view
    path('user/', RetrieveUserView.as_view(), name='user'),
    path('updateuser/', UpdateUserView.as_view(), name='updateuser'),
    path('deactivateuser/', DeactivateUserAccount.as_view(), name='deactivateuser'),
    
    #Category view
    path('createcategory/', CreateCategoryView.as_view(), name='createcategory'),
    path('listcategories/', ListCategoriesView.as_view(), name='listcategories'),
    path('retrievecategory/<str:slug>/', RetrieveCategoryView.as_view(), name='retrievecategory'),
    path('updatecategory/<str:slug>/<int:pk>/', UpdateCategoryView.as_view(), name='updatecategory'),
    path('deletecategory/<str:slug>/<int:pk>/', DeleteCategoryView.as_view(), name='deletecategory'),
    path('deactivatecategory/<str:slug>/<int:pk>/', DeactivateCategoryView.as_view(), name='deactivatecategory'),
    path('activatecategory/<str:slug>/<int:pk>/', ActivateCategoryView.as_view(), name='activatecategory'),
    
    #Product view
    path('createproduct/', CreateProductView.as_view(), name='createproduct'),
    path('listproducts/', ListProductsView.as_view(), name='listproduct'),
    path('productscategories/', ProductsCategoriesView.as_view(), name='productcategories'),
    path('productscategory/<str:slug>/', ProductsCategoryView.as_view(), name='productcategory'),
    path('retrieveproduct/<str:slug>/', RetrieveProductView.as_view(), name='productretrieve'),
    path('updateproduct/<str:slug>/<int:pk>/', UpdateProductView.as_view(), name='productupdate'),
    path('deleteproduct/<str:slug>/<int:pk>/', DeleteProductView.as_view(), name='productdelete'),
    path('deactivateproduct/<str:slug>/<int:pk>/', DeactivateProductView.as_view(), name='deactivateproduct'),
    path('activateproduct/<str:slug>/<int:pk>/', ActivateProductView.as_view(), name='activateproduct'),

    
    #Checkout
    path('checkout/', EpaycoCheckoutView.as_view(), name='checkout'),
    path('checkoutconfirmation/', EpaycoPaymentConfirmationView.as_view(), name='checkoutconfirmation'),
    path('epayco/response/', EpaycoResponseHTMLView.as_view(), name='epayco-response-html')
]
