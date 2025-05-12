import graphene
from graphene_django.types import DjangoObjectType
from restaurant.models import Category, Ingredient, Product, Order, OrderItem, OrderDetail
from django.contrib.auth.models import User


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "username", "email")


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = "__all__"


class IngredientType(DjangoObjectType):
    class Meta:
        model = Ingredient
        fields = "__all__"


class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = "__all__"


class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        fields = "__all__"


class OrderItemType(DjangoObjectType):
    class Meta:
        model = OrderItem
        fields = "__all__"


class OrderDetailType(DjangoObjectType):
    class Meta:
        model = OrderDetail
        fields = "__all__"