from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models


class Maquina(models.Model):
    class TipoImpressao(models.TextChoices):
        FDM = "FDM", "FDM"
        RESINA = "RESINA", "Resina"

    nome = models.CharField("nome", max_length=100)
    tipo_impressao = models.CharField(
        "tipo de impressão",
        max_length=10,
        choices=TipoImpressao.choices,
    )
    preco_compra = models.DecimalField(
        "preço de compra (R$)",
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    valor_revenda = models.DecimalField(
        "valor de revenda (R$)",
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    vida_util_horas = models.PositiveIntegerField(
        "vida útil (horas)",
        validators=[MinValueValidator(1)],
    )
    consumo_watts = models.PositiveIntegerField(
        "consumo médio (watts)",
        validators=[MinValueValidator(1)],
    )
    manutencao_por_hora = models.DecimalField(
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
            self.preco_compra is not None
            and self.valor_revenda is not None
            and self.valor_revenda > self.preco_compra
        ):
            raise ValidationError(
                {"valor_revenda": "O valor de revenda não pode superar o preço de compra."}
            )

    def __str__(self):
        return self.nome

    @property
    def depreciacao_por_hora(self):
        return (self.preco_compra - self.valor_revenda) / self.vida_util_horas

    @property
    def maquina_custo_por_hora(self):
        return self.depreciacao_por_hora + self.manutencao_por_hora
