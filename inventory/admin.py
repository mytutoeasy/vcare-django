from django.contrib import admin
from .models import InventoryItem

@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'category', 'quantity', 'reorder_level', 'is_low_stock', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'sku')
    list_editable = ('quantity', 'reorder_level')
