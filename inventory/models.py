"""
inventory/models.py
Inventory items with low-stock alerts
"""

from django.db import models
from django.core.validators import MinValueValidator
from patients.models import SoftDeleteModel


class InventoryItem(SoftDeleteModel):
    name = models.CharField(max_length=120)
    sku = models.CharField(max_length=50, unique=True, blank=True, null=True)
    category = models.CharField(max_length=60, blank=True)
    unit = models.CharField(max_length=20, default='pcs')
    quantity = models.PositiveIntegerField(default=0)
    reorder_level = models.PositiveIntegerField(
        default=10,
        help_text="Alert when quantity falls to this level or below"
    )
    unit_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)]
    )
    supplier = models.CharField(max_length=100, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['quantity', 'reorder_level']),
            models.Index(fields=['category']),
        ]

    def __str__(self):
        return f"{self.name} ({self.quantity} {self.unit})"

    @property
    def is_low_stock(self):
        return self.quantity <= self.reorder_level

    @property
    def stock_status(self):
        if self.quantity == 0:
            return 'out_of_stock'
        if self.is_low_stock:
            return 'low'
        return 'ok'
