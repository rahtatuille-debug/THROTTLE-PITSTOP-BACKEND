from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    # Matches the ProductImageInline pattern in apps/catalog/admin.py.
    model = OrderItem
    extra = 0
    readonly_fields = ("product", "product_name", "unit_price", "quantity")
    can_delete = False

    def has_add_permission(self, request, obj=None):
        # Order items are created at checkout time only, never by hand.
        return False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id", "customer_name", "order_total", "payment_method", "status", "created_at",
    )
    list_filter = ("status", "payment_method")
    list_editable = ("status",)
    search_fields = ("customer_name", "customer_phone")
    inlines = [OrderItemInline]

    def order_total(self, obj):
        return obj.total
    order_total.short_description = "Total"

    def save_model(self, request, obj, form, change):
        """
        Restore stock when an order is cancelled from the admin.

        Stock is decremented at order-creation time, not on payment
        confirmation (design decision 2.5) - a deliberate simplification
        to avoid overselling gear that's sitting in one physical shop.
        That means a cancelled order has to give its stock back by hand
        here, and only exactly once: we compare the status this row had
        in the database before this save against the incoming status, so
        re-saving an already-cancelled order (with no further status
        change) never restores stock twice, and this never fires on the
        initial create (there is no "previous" row to compare against).
        """
        previously_cancelled = False
        if change:
            previous = Order.objects.filter(pk=obj.pk).first()
            previously_cancelled = bool(
                previous and previous.status == Order.STATUS_CANCELLED
            )

        super().save_model(request, obj, form, change)

        just_cancelled = (
            change
            and obj.status == Order.STATUS_CANCELLED
            and not previously_cancelled
        )
        if just_cancelled:
            for item in obj.items.select_related("product"):
                product = item.product
                product.stock += item.quantity
                product.save(update_fields=["stock"])
