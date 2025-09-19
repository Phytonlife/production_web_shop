from django.db import transaction
from rest_framework import serializers
from .models import Cart, CartItem, Order, OrderItem
from products.serializers import ProductSerializer

# --- Cart Serializers ---

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity", "total_price"]

    def get_total_price(self, obj):
        return obj.quantity * obj.product.price

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_cart_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ["id", "user", "items", "total_cart_price"]

    def get_total_cart_price(self, obj):
        return sum(item.quantity * item.product.price for item in obj.items.all())

# --- Order Serializers ---

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "product", "quantity", "price"]

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    user = serializers.StringRelatedField()

    class Meta:
        model = Order
        fields = ["id", "user", "status", "total_amount", "created_at", "items"]

class OrderCreateSerializer(serializers.Serializer):
    cart_id = serializers.IntegerField()

    def validate_cart_id(self, cart_id):
        try:
            cart = Cart.objects.get(id=cart_id, user=self.context['request'].user)
            if not cart.items.exists():
                raise serializers.ValidationError("Cart is empty.")
        except Cart.DoesNotExist:
            raise serializers.ValidationError("Cart not found.")
        return cart_id

    def save(self, **kwargs):
        with transaction.atomic():
            cart = Cart.objects.get(id=self.validated_data['cart_id'])
            
            # Создание заказа
            order = Order.objects.create(
                user=cart.user,
                total_amount=sum(item.quantity * item.product.price for item in cart.items.all())
            )

            # Перенос товаров из корзины в заказ
            order_items_to_create = []
            for item in cart.items.all():
                order_items_to_create.append(
                    OrderItem(
                        order=order,
                        product=item.product,
                        quantity=item.quantity,
                        price=item.product.price # Фиксируем цену на момент покупки
                    )
                )
            OrderItem.objects.bulk_create(order_items_to_create)

            # Очистка корзины
            cart.items.all().delete()

            return order
