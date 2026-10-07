from django.contrib import admin

from .models import Material


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "material_type",
        "spool_price",
        "spool_weight_g",
        "price_per_gram_display",
    )
    list_filter = ("material_type",)
    search_fields = ("name",)

    @admin.display(description="Preço por grama (R$)")
    def price_per_gram_display(self, obj):
        return f"{obj.price_per_gram:.4f}"