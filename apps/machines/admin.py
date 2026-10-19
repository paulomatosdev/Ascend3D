from django.contrib import admin

from .models import Maquina


@admin.register(Maquina)
class MachineAdmin(admin.ModelAdmin):
    list_display = (
        "nome",
        "tipo_impressao",
        "preco_compra",
        "machine_cost_per_hour_display",
    )
    list_filter = ("tipo_impressao",)
    search_fields = ("nome",)

    @admin.display(description="Custo de máquina por hora (R$)")
    def machine_cost_per_hour_display(self, obj):
        return f"{obj.machine_cost_per_hour:.2f}"
