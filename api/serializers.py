from django.contrib.auth.models import User
from rest_framework import serializers

from restaurant.models import Category, Ingredient, Product, OrderItem, Order, OrderDetail


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'url', 'name']


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'url', 'name', 'is_allergen']


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )
    ingredients = IngredientSerializer(read_only=True, many=True)
    ingredient_ids = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(), many=True, source='ingredients', write_only=True
    )

    class Meta:
        model = Product
        fields = ['id', 'url', 'name', 'description', 'price', 'image',
                  'category', 'category_id', 'ingredients', 'ingredient_ids']


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True
    )

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_id', 'quantity']


class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        exclude = ['order']


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    items = OrderItemSerializer(many=True)
    details = OrderDetailSerializer(required=False)
    total_value = serializers.FloatField(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'url', 'user', 'items', 'details', 'status', 'created_at', 'total_value']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        details_data = validated_data.pop('details', None)
        user = validated_data.pop('user')
        order = Order.objects.create(user=self.context['request'].user, **validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)

        if details_data:
            OrderDetail.objects.create(order=order, **details_data)

        return order


class OrderOnlyCreateSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'url', 'user', 'status', 'created_at']

    def create(self, validated_data):
        user = validated_data.pop('user')
        order = Order.objects.create(user=self.context['request'].user, **validated_data)

        return order


class OrderItemOnlyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'quantity']


class OrderDetailOnlyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = ['id', 'order', 'delivery_notes', 'delivery_address', 'phone_number']