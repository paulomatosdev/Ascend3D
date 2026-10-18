from django.contrib import admin

from .models import SalesChannel


@admin.register(SalesChannel)
class SalesChannelAdmin(admin.ModelAdmin):
    list_display = ("name", "commission_percent", "fixed_fee")
    search_fields = ("name",)
    