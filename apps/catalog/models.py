from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models


class Material(models.Model):
    class MaterialType(models.TextChoices):
        PLA = "PLA", "PLA"
        PETG = "PETG", "PETG"
        ABS = "ABS", "ABS"
        TPU = "TPU", "TPU"
        RESIN = "RESINA", "Resina"
        OTHER = "OUTRO", "Outro"

    name = models.CharField("nome", max_length=100)
    material_type = models.CharField(
        "tipo", max_length=10, choices=MaterialType.choices
    )
    spool_price = models.DecimalField(
        "preço do rolo (R$)",
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    spool_weight_g = models.PositiveIntegerField(
        "peso do rolo (g)",
        validators=[MinValueValidator(1)],
    )
    created_at = models.DateTimeField("criado em", auto_now_add=True)

    class Meta:
        verbose_name = "material"
        verbose_name_plural = "materiais"
        ordering = ["name"]

    def __str__(self):
        return self.name

    @property
    def price_per_gram(self):
        return self.spool_price / self.spool_weight_g