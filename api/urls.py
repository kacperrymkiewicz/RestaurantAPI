from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import CategoryListCreateView, CategoryDetailView, IngredientListCreateView, \
    IngredientDetailView, ProductListCreateView, ProductDetailView, OrderListCreateView, OrderDetailView, \
    OrderDetailOnlyCreateView, APIRootView, OrderOnlyCreateView, OrderItemOnlyCreateView, OrderUpdateDeleteView, \
    OrderItemUpdateDeleteView, OrderDetailUpdateDeleteView

urlpatterns = [
    # JWT
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('', APIRootView.as_view(), name='api-root'),

    # Category
    path('categories/', CategoryListCreateView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),

    # Ingredient
    path('ingredients/', IngredientListCreateView.as_view(), name='ingredient-list'),
    path('ingredients/<int:pk>/', IngredientDetailView.as_view(), name='ingredient-detail'),

    # Product
    path('products/', ProductListCreateView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),

    # Order
    path('orders/', OrderListCreateView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),

    path('order/', OrderOnlyCreateView.as_view(), name='order-create'),
    path('order/<int:pk>/', OrderUpdateDeleteView.as_view(), name='order-edit-delete'),

    path('order-items/', OrderItemOnlyCreateView.as_view(), name='orderitem-create'),
    path('order-items/<int:pk>/', OrderItemUpdateDeleteView.as_view(), name='orderitem-edit-delete'),

    path('order-details/', OrderDetailOnlyCreateView.as_view(), name='orderdetail-create'),
    path('order-details/<int:pk>/', OrderDetailUpdateDeleteView.as_view(), name='orderdetail-edit-delete')

]