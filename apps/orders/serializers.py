from django.db import transaction
from rest_framework import serializers
from apps.catalog.models import Product
from .models import Order, OrderItem


class OrderItemCreateSerializer(serializers.Serializer):
    """Not a ModelSerializer - this only validates the shape of one cart
    line as posted by the frontend ({product_id, quantity}); the actual
    OrderItem rows are built by hand in OrderCreateSerializer.create()
    so we can snapshot product_name/unit_price and decrement stock."""
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)


class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemCreateSerializer(many=True, write_only=True)

    class Meta:
        model = Order
        fields = (
            "id", "customer_name", "customer_phone", "delivery_address",
            "payment_method", "notes", "items",
        )
        read_only_fields = ("id",)

    def validate_items(self, items):
        if not items:
            raise serializers.ValidationError("Your cart is empty.")

        product_ids = [item["product_id"] for item in items]
        products = Product.objects.filter(id__in=product_ids, is_active=True)
        products_by_id = {p.id: p for p in products}

        errors = []
        for item in items:
            product = products_by_id.get(item["product_id"])
            if product is None:
                errors.append(
                    f"Product {item['product_id']} is no longer available."
                )
                continue
            if item["quantity"] > product.stock:
                errors.append(
                    f"Only {product.stock} left of \"{product.name}\" "
                    f"(requested {item['quantity']})."
                )

        if errors:
            raise serializers.ValidationError(errors)

        return items

    @transaction.atomic
    def create(self, validated_data):
        items_data = validated_data.pop("items")
        order = Order.objects.create(**validated_data)

        # Re-fetch inside the atomic block with select_for_update so two
        # near-simultaneous checkouts for the last unit of stock can't
        # both succeed.
        product_ids = [item["product_id"] for item in items_data]
        products_by_id = {
            p.id: p
            for p in Product.objects.select_for_update().filter(id__in=product_ids)
        }

        for item in items_data:
            product = products_by_id[item["product_id"]]
            quantity = item["quantity"]
            if quantity > product.stock:
                raise serializers.ValidationError(
                    f"Only {product.stock} left of \"{product.name}\" "
                    f"(requested {quantity})."
                )
            OrderItem.objects.create(
                order=order,
                product=product,
                product_name=product.name,
                unit_price=product.price,
                quantity=quantity,
            )
            product.stock -= quantity
            product.save(update_fields=["stock"])

        return order


class OrderItemDetailSerializer(serializers.ModelSerializer):
    line_total = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = ("id", "product", "product_name", "unit_price", "quantity", "line_total")


class OrderDetailSerializer(serializers.ModelSerializer):
    items = OrderItemDetailSerializer(many=True, read_only=True)
    total = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = (
            "id", "customer_name", "customer_phone", "delivery_address",
            "payment_method", "status", "notes", "items", "total", "created_at",
        )
