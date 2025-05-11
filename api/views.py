from django.db.models import Sum, F, FloatField
from django.shortcuts import render

from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from restaurant.models import Category, Ingredient, Product, Order, OrderItem, OrderDetail
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from .serializers import CategorySerializer, IngredientSerializer, ProductSerializer, OrderSerializer, \
    OrderItemSerializer, OrderDetailSerializer, OrderOnlyCreateSerializer, OrderItemOnlyCreateSerializer, \
    OrderDetailOnlyCreateSerializer


class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class IngredientListCreateView(generics.ListCreateAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [IsAdminOrReadOnly]


class IngredientDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [IsAdminOrReadOnly]


class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]


class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderOnlyCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderOnlyCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OrderItemOnlyCreateView(generics.CreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemOnlyCreateSerializer
    permission_classes = [permissions.IsAuthenticated]


class OrderDetailOnlyCreateView(generics.CreateAPIView):
    queryset = OrderDetail.objects.all()
    serializer_class = OrderDetailOnlyCreateSerializer
    permission_classes = [permissions.IsAuthenticated]


class OrderUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderOnlyCreateSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


class OrderItemUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemOnlyCreateSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


class OrderDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderDetail.objects.all()
    serializer_class = OrderDetailOnlyCreateSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


class UserOrderStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        total_spent = Order.objects.filter(user=request.user).aggregate(
            total=Sum(F('items__quantity') * F('items__product__price'))
        )['total'] or 0
        return Response({
            'user': request.user.username,
            'total_spent': round(total_spent, 2)
        })


class OrderWithTotalValueView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).annotate(
            total_value=Sum(F('items__quantity') * F('items__product__price'), output_field=FloatField())
        )


class APIRootView(APIView):
    def get(self, request, format=None):
        return Response({
            'orders': reverse('order-list', request=request, format=format),
            'orders-stats': reverse('order-user-stats', request=request, format=format),
            'orders-with-total': reverse('orders-with-total', request=request, format=format),
            'products': reverse('product-list', request=request, format=format),
            'categories': reverse('category-list', request=request, format=format),
            'ingredients': reverse('ingredient-list', request=request, format=format),
            'order-create': reverse('order-create', request=request, format=format),
            'orderitem-create': reverse('orderitem-create', request=request, format=format),
            'orderdetail-create': reverse('orderdetail-create', request=request, format=format),
        })