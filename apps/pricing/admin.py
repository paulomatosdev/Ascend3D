from django.contrib import admin

from .models import PerfilPrecificacao


@admin.register(PerfilPrecificacao)
class PerfilPrecificacaoAdmin(admin.ModelAdmin):
    list_display = ("nome", "tarifa_Kwh", "valor_hora_trabalhada", "porcentagem_falha", "markup")
    search_fields = ("nome",)
