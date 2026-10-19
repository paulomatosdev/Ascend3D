from decimal import Decimal, ROUND_HALF_UP

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

class Marketplaces(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    porcentagem_comissao = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00")), MaxValueValidator(Decimal("99.99"))],
    )
    taxa_fixa = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def taxa_comissao(self):
        return self.porcentagem_comissao / Decimal("100")

    def valor_venda(self, valor_liq):
        preco = (valor_liq + self.taxa_fixa) / (1 - self.taxa_comissao)
        return preco.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


    def __str__(self):
        return self.nome
