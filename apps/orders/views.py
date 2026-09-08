from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Order
from .serializers import OrderCreateSerializer, OrderDetailSerializer


class OrderCreateView(generics.CreateAPIView):
    """POST /api/orders/ - guest checkout, no auth required (design decision 2.4)."""
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save(
            user=request.user if request.user.is_authenticated else None
        )
        detail = OrderDetailSerializer(order)
        headers = self.get_success_headers(detail.data)
        return Response(detail.data, status=status.HTTP_201_CREATED, headers=headers)


class OrderDetailView(generics.RetrieveAPIView):
    """
    GET /api/orders/<id>/ - used by the order-confirmation/tracking page.

    Deliberately public-by-id (no auth) since checkout is guest-friendly
    and there's no logged-in user to check ownership against in the
    common case - see handoff Section 3.2.4. An order id isn't
    realistically enumerable at this shop's scale. There is intentionally
    no list endpoint at this permission level (see urls.py).
    """
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "pk"
