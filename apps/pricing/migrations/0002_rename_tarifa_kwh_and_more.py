# Rename the electricity-rate field and enforce a positive minimum.

import django.core.validators
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pricing", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="perfilprecificacao",
            old_name="tarifa_Kwh",
            new_name="tarifa_kwh",
        ),
        migrations.AlterField(
            model_name="perfilprecificacao",
            name="tarifa_kwh",
            field=models.DecimalField(
                decimal_places=2,
                max_digits=10,
                validators=[django.core.validators.MinValueValidator(Decimal("0.01"))],
                verbose_name="Tarifa KWh",
            ),
        ),
    ]
