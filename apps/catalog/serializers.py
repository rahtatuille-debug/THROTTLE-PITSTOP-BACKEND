from rest_framework import serializers
from .models import Category, Product, ProductImage


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "slug")


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ("id", "image", "is_primary", "alt_text")


class ProductListSerializer(serializers.ModelSerializer):
    """Lighter serializer for the shop grid - avoids sending full description."""
    category = CategorySerializer(read_only=True)
    primary_image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ("id", "name", "slug", "price", "in_stock", "category", "primary_image")

    def get_primary_image(self, obj):
        image = obj.images.first()
        if not image:
            return None
        request = self.context.get("request")
        url = image.image.url
        return request.build_absolute_uri(url) if request else url


class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = (
            "id", "name", "slug", "description", "price",
            "stock", "in_stock", "category", "images",
        )
