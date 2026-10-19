from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase

from .models import Maquina


class MachineCostTests(TestCase):
    def setUp(self):
        self.maquinas = Maquina(
            nome="Impressora de teste",
            tipo_impressao=Maquina.Tipo_Impressao.FDM,
            preco_compra=Decimal("3000.00"),
            valor_revenda=Decimal("600.00"),
            vida_util_horas=3000,
            consumo_watts=150,
            manutencao_por_hora=Decimal("0.30"),
        )

    def test_calculates_depreciation_and_machine_cost_per_hour(self):
        self.assertEqual(self.maquinas.depreciacao_por_hora, Decimal("0.80"))
        self.assertEqual(self.maquinas.maquina_custo_por_hora, Decimal("1.10"))

    def test_zero_resale_value_depreciates_full_purchase_price(self):
        self.maquinas.valor_revenda = Decimal("0.00")

        self.assertEqual(self.maquinas.depreciacao_por_hora, Decimal("1.00"))

    def test_resale_value_greater_than_purchase_price_fails_validation(self):
        self.maquinas.valor_revenda = Decimal("3000.01")

        with self.assertRaises(ValidationError) as raised:
            self.maquinas.full_clean()

        self.assertIn("valor_revenda", raised.exception.message_dict)

    def test_zero_life_span_fails_validation(self):
        self.maquinas.vida_util_horas = 0

        with self.assertRaises(ValidationError) as raised:
            self.maquinas.full_clean()

        self.assertIn("vida_util_horas", raised.exception.message_dict)

    def test_valid_machine_passes_validation(self):
        self.maquinas.full_clean()

    def test_resale_value_equal_to_purchase_price_passes_validation(self):
        self.maquinas.valor_revenda = Decimal("3000.00")

        self.maquinas.full_clean()

        self.assertEqual(self.maquinas.depreciacao_por_hora, Decimal("0.00"))

    def test_non_positive_purchase_price_fails_validation(self):
        for value in (Decimal("0.00"), Decimal("-1.00")):
            with self.subTest(purchase_price=value):
                self.maquinas.preco_compra = value

                with self.assertRaises(ValidationError) as raised:
                    self.maquinas.full_clean()

                self.assertIn("preco_compra", raised.exception.message_dict)

    def test_negative_maintenance_fails_validation(self):
        self.maquinas.manutencao_por_hora = Decimal("-0.01")

        with self.assertRaises(ValidationError) as raised:
            self.maquinas.full_clean()

        self.assertIn("manutencao_por_hora", raised.exception.message_dict)

    def test_zero_maintenance_is_valid(self):
        self.maquinas.manutencao_por_hora = Decimal("0.00")

        self.maquinas.full_clean()

        self.assertEqual(self.maquinas.maquina_custo_por_hora, Decimal("0.80"))
