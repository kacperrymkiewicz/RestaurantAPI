import graphene
from .types import *
from restaurant.models import *


class Query(graphene.ObjectType):
    all_categories = graphene.List(CategoryType)
    all_ingredients = graphene.List(IngredientType)
    all_products = graphene.List(ProductType)
    all_orders = graphene.List(OrderType)
    all_order_items = graphene.List(OrderItemType)
    all_order_details = graphene.List(OrderDetailType)
    all_users = graphene.List(UserType)

    def resolve_all_categories(self, info):
        return Category.objects.all()

    def resolve_all_ingredients(self, info):
        return Ingredient.objects.all()

    def resolve_all_products(self, info):
        return Product.objects.all()

    def resolve_all_orders(self, info):
        return Order.objects.all()

    def resolve_all_order_items(self, info):
        return OrderItem.objects.all()

    def resolve_all_order_details(self, info):
        return OrderDetail.objects.all()

    def resolve_all_users(self, info):
        return User.objects.all()