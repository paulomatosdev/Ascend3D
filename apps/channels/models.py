from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

class SalesChannel(models.Model):
    name = models.CharField(max_length=100, unique=True)
    commission_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00")), MaxValueValidator(Decimal("99.99"))],
    )
    fixed_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def commission_rate(self):
        return self.commission_percent / Decimal("100")

    def price_to_receive(self, net_amount):
        price = (net_amount + self.fixed_fee) / (1 - self.commission_rate)
        return price.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


    def __str__(self):
        return self.name
