from decimal import Decimal

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class PerfilPrecificacao(models.Model):
    nome = models.CharField("Nome", max_length=100, unique=True)
    tarifa_kwh = models.DecimalField(
        "Tarifa KWh",
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    valor_hora_trabalhada = models.DecimalField(
        "Valor Hora Trabalhada", max_digits=10, decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    porcentagem_falha = models.DecimalField(
        "Porcentagem de Falha", max_digits=5, decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00")), MaxValueValidator(Decimal("99.99"))],
    )
    custo_embalagem = models.DecimalField(
        "Custo de Embalagem", max_digits=10, decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    markup = models.DecimalField(
        "Markup", max_digits=5, decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    created_at = models.DateTimeField("Data de Criação", auto_now_add=True)

    class Meta:
        verbose_name = "perfil de precificação"
        verbose_name_plural = "perfis de precificação"
        ordering = ["nome"]

    def __str__(self):
        return self.nome

    @property
    def taxa_falha(self):
        return self.porcentagem_falha / Decimal("100")

    @property
    def markup_fracao(self):
        return self.markup / Decimal("100")
