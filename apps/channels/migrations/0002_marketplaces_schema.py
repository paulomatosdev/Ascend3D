# Corrige o esquema legado SalesChannel para o modelo atual Marketplaces.
import decimal
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("channels", "0001_initial")]

    operations = [
        migrations.DeleteModel(name="SalesChannel"),
        migrations.CreateModel(
            name="Marketplaces",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nome", models.CharField(max_length=100, unique=True)),
                ("porcentagem_comissao", models.DecimalField(
                    max_digits=5, decimal_places=2,
                    validators=[MinValueValidator(decimal.Decimal("0.00")), MaxValueValidator(decimal.Decimal("99.99"))],
                )),
                ("taxa_fixa", models.DecimalField(
                    max_digits=10, decimal_places=2,
                    validators=[MinValueValidator(decimal.Decimal("0.00"))],
                )),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
