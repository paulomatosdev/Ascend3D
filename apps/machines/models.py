from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models


class Machine(models.Model):
    class Technology(models.TextChoices):
        FDM = "FDM", "FDM"
        RESINA = "RESINA", "Resina"

    name = models.CharField("nome", max_length=100)
    technology = models.CharField(
        "tipo de impressão",
        max_length=10,
        choices=Technology.choices,
    )
    purchase_price = models.DecimalField(
        "preço de compra (R$)",
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    resale_value = models.DecimalField(
        "valor de revenda (R$)",
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    life_span_hours = models.PositiveIntegerField(
        "vida útil (horas)",
        validators=[MinValueValidator(1)],
    )
    avg_power_watts = models.PositiveIntegerField(
        "consumo médio (watts)",
        validators=[MinValueValidator(1)],
    )
    maintenance_per_hour = models.DecimalField(
        "manutenção por hora (R$)",
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
    )

    created_at = models.DateTimeField("criado em", auto_now_add=True)

    class Meta:
        verbose_name = "impressora"
        verbose_name_plural = "impressoras"

    def clean(self):
        super().clean()
        if (
            self.purchase_price is not None
            and self.resale_value is not None
            and self.resale_value > self.purchase_price
        ):
            raise ValidationError(
                {"resale_value": "O valor de revenda não pode superar o preço de compra."}
            )

    def __str__(self):
        return self.name

    @property
    def depreciation_per_hour(self):
        return (self.purchase_price - self.resale_value) / self.life_span_hours

    @property
    def machine_cost_per_hour(self):
        return self.depreciation_per_hour + self.maintenance_per_hour
