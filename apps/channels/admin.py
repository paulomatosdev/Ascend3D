from django.contrib import admin

from .models import Marketplaces


@admin.register(Marketplaces)
class MarketplaceAdmin(admin.ModelAdmin):
    list_display = ("nome", "porcentagem_comissao", "taxa_fixa")
    search_fields = ("nome",)
    