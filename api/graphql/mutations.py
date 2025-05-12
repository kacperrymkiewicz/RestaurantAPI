import graphene
from graphql_jwt.decorators import login_required

from restaurant.models import *
from .types import *
from django.contrib.auth.models import User


class CreateOrder(graphene.Mutation):
    class Arguments:
        status = graphene.String(required=False)

    order = graphene.Field(OrderType)

    @login_required
    def mutate(self, info, status="pending"):
        user = info.context.user
        order = Order.objects.create(user=user, status=status)
        return CreateOrder(order=order)


class CreateOrderItem(graphene.Mutation):
    class Arguments:
        order_id = graphene.ID(required=True)
        product_id = graphene.ID(required=True)
        quantity = graphene.Int(required=True)

    order_item = graphene.Field(OrderItemType)

    def mutate(self, info, order_id, product_id, quantity):
        order = Order.objects.get(pk=order_id)
        product = Product.objects.get(pk=product_id)
        item = OrderItem.objects.create(order=order, product=product, quantity=quantity)
        return CreateOrderItem(order_item=item)


class CreateOrderDetail(graphene.Mutation):
    class Arguments:
        order_id = graphene.ID(required=True)
        delivery_notes = graphene.String()
        delivery_address = graphene.String(required=True)
        phone_number = graphene.String(required=True)

    order_detail = graphene.Field(OrderDetailType)

    def mutate(self, info, order_id, delivery_notes="", delivery_address="", phone_number=""):
        order = Order.objects.get(pk=order_id)
        details = OrderDetail.objects.create(
            order=order,
            delivery_notes=delivery_notes,
            delivery_address=delivery_address,
            phone_number=phone_number
        )
        return CreateOrderDetail(order_detail=details)


class Mutation(graphene.ObjectType):
    create_order = CreateOrder.Field()
    create_order_item = CreateOrderItem.Field()
    create_order_detail = CreateOrderDetail.Field()
