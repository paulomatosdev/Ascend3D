from django.contrib import admin

from .models import Machine


@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "technology",
        "purchase_price",
        "machine_cost_per_hour_display",
    )
    list_filter = ("technology",)
    search_fields = ("name",)

    @admin.display(description="Custo de máquina por hora (R$)")
    def machine_cost_per_hour_display(self, obj):
        return f"{obj.machine_cost_per_hour:.2f}"
