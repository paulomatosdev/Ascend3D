from django.contrib import admin

from .models import Maquina


@admin.register(Maquina)
class MaquinaAdmin(admin.ModelAdmin):
    list_display = (
        "nome",
        "tipo_impressao",
        "preco_compra",
        "maquina_custo_por_hora_display",
    )
    list_filter = ("tipo_impressao",)
    search_fields = ("nome",)

    @admin.display(description="Custo de máquina por hora (R$)")
    def maquina_custo_por_hora_display(self, obj):
        return f"{obj.maquina_custo_por_hora:.2f}"
