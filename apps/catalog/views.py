from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Product
from .serializers import CategorySerializer, ProductListSerializer, ProductDetailSerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "slug"


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only from the API - products are managed in Django admin.
    Supports ?category=<slug> and ?search=<text> via query params.
    """
    queryset = Product.objects.filter(is_active=True).select_related("category").prefetch_related("images")
    lookup_field = "slug"
    filterset_fields = ["category__slug"]

    def get_serializer_class(self):
        if self.action == "list":
            return ProductListSerializer
        return ProductDetailSerializer
