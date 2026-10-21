from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase

from .models import PerfilPrecificacao


class PerfilPrecificacaoValidationTests(TestCase):
    def make_perfil(self, **overrides):
        data = {
            "nome": "Perfil 1",
            "tarifa_kwh": Decimal("0.50"),
            "valor_hora_trabalhada": Decimal("20.00"),
            "porcentagem_falha": Decimal("5.00"),
            "custo_embalagem": Decimal("2.00"),
            "markup": Decimal("10.00"),
        }
        data.update(overrides)
        return PerfilPrecificacao(**data)

    def assert_invalid(self, perfil, field):
        with self.assertRaises(ValidationError) as raised:
            perfil.full_clean()
        self.assertIn(field, raised.exception.message_dict)

    def test_valid_perfil_passes_validation(self):
        self.make_perfil().full_clean()

    def test_positive_electricity_rate_passes_validation(self):
        self.make_perfil(tarifa_kwh=Decimal("0.01")).full_clean()

    def test_zero_electricity_rate_fails_validation(self):
        self.assert_invalid(self.make_perfil(tarifa_kwh=Decimal("0.00")), "tarifa_kwh")

    def test_zero_hourly_labor_value_passes_validation(self):
        self.make_perfil(valor_hora_trabalhada=Decimal("0.00")).full_clean()

    def test_negative_hourly_labor_value_fails_validation(self):
        self.assert_invalid(
            self.make_perfil(valor_hora_trabalhada=Decimal("-0.01")),
            "valor_hora_trabalhada",
        )

    def test_maximum_failure_percentage_passes_validation(self):
        self.make_perfil(porcentagem_falha=Decimal("99.99")).full_clean()

    def test_failure_percentage_of_100_fails_validation(self):
        self.assert_invalid(self.make_perfil(porcentagem_falha=Decimal("100")), "porcentagem_falha")

    def test_negative_failure_percentage_fails_validation(self):
        self.assert_invalid(self.make_perfil(porcentagem_falha=Decimal("-1")), "porcentagem_falha")

    def test_negative_packaging_cost_fails_validation(self):
        self.assert_invalid(self.make_perfil(custo_embalagem=Decimal("-0.01")), "custo_embalagem")

    def test_markup_of_150_passes_validation(self):
        self.make_perfil(markup=Decimal("150.00")).full_clean()

    def test_negative_markup_fails_validation(self):
        self.assert_invalid(self.make_perfil(markup=Decimal("-0.01")), "markup")

    def test_failure_percentage_converts_to_fraction(self):
        perfil = self.make_perfil(porcentagem_falha=Decimal("10.00"))

        self.assertEqual(perfil.taxa_falha, Decimal("0.10"))

    def test_markup_converts_to_fraction(self):
        perfil = self.make_perfil(markup=Decimal("100.00"))

        self.assertEqual(perfil.markup_fracao, Decimal("1.00"))

    def test_blank_name_fails_validation(self):
        self.assert_invalid(self.make_perfil(nome=""), "nome")

    def test_duplicate_name_fails_validation(self):
        self.make_perfil().save()
        self.assert_invalid(self.make_perfil(), "nome")
