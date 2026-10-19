# Initial migration for pricing profiles.
import decimal
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="PerfilPrecificacao",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nome", models.CharField(max_length=100, unique=True, verbose_name="Nome")),
                ("tarifa_Kwh", models.DecimalField(decimal_places=2, max_digits=10, validators=[MinValueValidator(decimal.Decimal("0.00"))], verbose_name="Tarifa KWh")),
                ("valor_hora_trabalhada", models.DecimalField(decimal_places=2, max_digits=10, validators=[MinValueValidator(decimal.Decimal("0.00"))], verbose_name="Valor Hora Trabalhada")),
                ("porcentagem_falha", models.DecimalField(decimal_places=2, max_digits=5, validators=[MinValueValidator(decimal.Decimal("0.00")), MaxValueValidator(decimal.Decimal("99.99"))], verbose_name="Porcentagem de Falha")),
                ("custo_embalagem", models.DecimalField(decimal_places=2, max_digits=10, validators=[MinValueValidator(decimal.Decimal("0.00"))], verbose_name="Custo de Embalagem")),
                ("markup", models.DecimalField(decimal_places=2, max_digits=5, validators=[MinValueValidator(decimal.Decimal("0.00"))], verbose_name="Markup")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")),
            ],
            options={"verbose_name": "perfil de precificação", "verbose_name_plural": "perfis de precificação", "ordering": ["nome"]},
        ),
    ]
