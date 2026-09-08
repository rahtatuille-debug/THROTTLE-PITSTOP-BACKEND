"""
Usage: python manage.py seed_catalog
Creates a handful of categories and dummy products so you have
something to look at in the admin and on the storefront right away.
"""
from django.core.management.base import BaseCommand
from apps.catalog.models import Category, Product


CATEGORIES = ["Helmets", "Jackets", "Gloves", "Boots", "Spare Parts"]

PRODUCTS = [
    ("AGV K1 Full-Face Helmet", "Helmets", 18500, 12,
     "DOT-certified full-face helmet with reinforced polycarbonate shell and removable liner."),
    ("Scoyco Riding Jacket", "Jackets", 9500, 8,
     "Abrasion-resistant riding jacket with CE-rated shoulder and elbow armor."),
    ("Pro Grip Leather Gloves", "Gloves", 2800, 20,
     "Full-grip leather gloves with knuckle protection, built for daily commuting."),
    ("Alpinestars Touring Boots", "Boots", 12500, 6,
     "Waterproof touring boots with reinforced ankle support."),
    ("Motorcycle Chain & Sprocket Kit", "Spare Parts", 4200, 15,
     "Heavy-duty chain and sprocket kit compatible with most 125-250cc bikes."),
]


class Command(BaseCommand):
    help = "Seeds the catalog with sample categories and products."

    def handle(self, *args, **options):
        cat_objs = {}
        for name in CATEGORIES:
            cat, created = Category.objects.get_or_create(name=name)
            cat_objs[name] = cat
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created category: {name}"))

        for name, cat_name, price, stock, description in PRODUCTS:
            product, created = Product.objects.get_or_create(
                name=name,
                defaults={
                    "category": cat_objs[cat_name],
                    "price": price,
                    "stock": stock,
                    "description": description,
                },
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created product: {name}"))

        self.stdout.write(self.style.SUCCESS("Catalog seeding complete."))
