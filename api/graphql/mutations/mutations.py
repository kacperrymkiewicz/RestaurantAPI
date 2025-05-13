import graphene
from graphql_jwt.decorators import login_required

from restaurant.models import *
from api.graphql.types import *
from django.contrib.auth.models import User

from .admin_mutations import (
    CreateCategory, UpdateCategory, DeleteCategory,
    CreateIngredient, UpdateIngredient, DeleteIngredient,
    CreateProduct, UpdateProduct, DeleteProduct
)


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

    @login_required
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

    @login_required
    def mutate(self, info, order_id, delivery_notes="", delivery_address="", phone_number=""):
        order = Order.objects.get(pk=order_id)
        details = OrderDetail.objects.create(
            order=order,
            delivery_notes=delivery_notes,
            delivery_address=delivery_address,
            phone_number=phone_number
        )
        return CreateOrderDetail(order_detail=details)


class UpdateOrder(graphene.Mutation):
    class Arguments:
        order_id = graphene.ID(required=True)
        status = graphene.String(required=True)

    order = graphene.Field(OrderType)

    @login_required
    def mutate(self, info, order_id, status):
        user = info.context.user
        order = Order.objects.get(pk=order_id)

        if order.user != user:
            raise Exception("You can only update your own orders.")

        order.status = status
        order.save()
        return UpdateOrder(order=order)


class UpdateOrderItem(graphene.Mutation):
    class Arguments:
        item_id = graphene.ID(required=True)
        quantity = graphene.Int(required=True)

    order_item = graphene.Field(OrderItemType)

    @login_required
    def mutate(self, info, item_id, quantity):
        item = OrderItem.objects.get(pk=item_id)
        if item.order.user != info.context.user:
            raise Exception("You can only update your own order items.")

        item.quantity = quantity
        item.save()
        return UpdateOrderItem(order_item=item)


class UpdateOrderDetail(graphene.Mutation):
    class Arguments:
        detail_id = graphene.ID(required=True)
        delivery_notes = graphene.String()
        delivery_address = graphene.String()
        phone_number = graphene.String()

    order_detail = graphene.Field(OrderDetailType)

    @login_required
    def mutate(self, info, detail_id, delivery_notes="", delivery_address="", phone_number=""):
        detail = OrderDetail.objects.get(pk=detail_id)

        if detail.order.user != info.context.user:
            raise Exception("You can only update your own order details.")

        if delivery_notes is not None:
            detail.delivery_notes = delivery_notes
        if delivery_address is not None:
            detail.delivery_address = delivery_address
        if phone_number is not None:
            detail.phone_number = phone_number

        detail.save()
        return UpdateOrderDetail(order_detail=detail)


class DeleteOrder(graphene.Mutation):
    class Arguments:
        order_id = graphene.ID(required=True)

    ok = graphene.Boolean()

    @login_required
    def mutate(self, info, order_id):
        order = Order.objects.get(pk=order_id)
        if order.user != info.context.user:
            raise Exception("You can only delete your own orders.")
        order.delete()
        return DeleteOrder(ok=True)


class DeleteOrderItem(graphene.Mutation):
    class Arguments:
        item_id = graphene.ID(required=True)

    ok = graphene.Boolean()

    @login_required
    def mutate(self, info, item_id):
        item = OrderItem.objects.get(pk=item_id)
        if item.order.user != info.context.user:
            raise Exception("You can only delete your own order items.")
        item.delete()
        return DeleteOrderItem(ok=True)


class DeleteOrderDetail(graphene.Mutation):
    class Arguments:
        detail_id = graphene.ID(required=True)

    ok = graphene.Boolean()

    @login_required
    def mutate(self, info, detail_id):
        detail = OrderDetail.objects.get(pk=detail_id)
        if detail.order.user != info.context.user:
            raise Exception("You can only delete your own order details.")
        detail.delete()
        return DeleteOrderDetail(ok=True)

class Mutation(graphene.ObjectType):
    create_order = CreateOrder.Field()
    create_order_item = CreateOrderItem.Field()
    create_order_detail = CreateOrderDetail.Field()

    update_order = UpdateOrder.Field()
    update_order_item = UpdateOrderItem.Field()
    update_order_detail = UpdateOrderDetail.Field()

    delete_order = DeleteOrder.Field()
    delete_order_item = DeleteOrderItem.Field()
    delete_order_detail = DeleteOrderDetail.Field()

    create_category = CreateCategory.Field()
    update_category = UpdateCategory.Field()
    delete_category = DeleteCategory.Field()

    create_ingredient = CreateIngredient.Field()
    update_ingredient = UpdateIngredient.Field()
    delete_ingredient = DeleteIngredient.Field()

    create_product = CreateProduct.Field()
    update_product = UpdateProduct.Field()
    delete_product = DeleteProduct.Field()