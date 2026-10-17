from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase

from .models import Machine


class MachineCostTests(TestCase):
    def setUp(self):
        self.machine = Machine(
            name="Impressora de teste",
            technology=Machine.Technology.FDM,
            purchase_price=Decimal("3000.00"),
            resale_value=Decimal("600.00"),
            life_span_hours=3000,
            avg_power_watts=150,
            maintenance_per_hour=Decimal("0.30"),
        )

    def test_calculates_depreciation_and_machine_cost_per_hour(self):
        self.assertEqual(self.machine.depreciation_per_hour, Decimal("0.80"))
        self.assertEqual(self.machine.machine_cost_per_hour, Decimal("1.10"))

    def test_zero_resale_value_depreciates_full_purchase_price(self):
        self.machine.resale_value = Decimal("0.00")

        self.assertEqual(self.machine.depreciation_per_hour, Decimal("1.00"))

    def test_resale_value_greater_than_purchase_price_fails_validation(self):
        self.machine.resale_value = Decimal("3000.01")

        with self.assertRaises(ValidationError) as raised:
            self.machine.full_clean()

        self.assertIn("resale_value", raised.exception.message_dict)

    def test_zero_life_span_fails_validation(self):
        self.machine.life_span_hours = 0

        with self.assertRaises(ValidationError) as raised:
            self.machine.full_clean()

        self.assertIn("life_span_hours", raised.exception.message_dict)

    def test_valid_machine_passes_validation(self):
        self.machine.full_clean()

    def test_resale_value_equal_to_purchase_price_passes_validation(self):
        self.machine.resale_value = Decimal("3000.00")

        self.machine.full_clean()

        self.assertEqual(self.machine.depreciation_per_hour, Decimal("0.00"))

    def test_non_positive_purchase_price_fails_validation(self):
        for value in (Decimal("0.00"), Decimal("-1.00")):
            with self.subTest(purchase_price=value):
                self.machine.purchase_price = value

                with self.assertRaises(ValidationError) as raised:
                    self.machine.full_clean()

                self.assertIn("purchase_price", raised.exception.message_dict)

    def test_negative_maintenance_fails_validation(self):
        self.machine.maintenance_per_hour = Decimal("-0.01")

        with self.assertRaises(ValidationError) as raised:
            self.machine.full_clean()

        self.assertIn("maintenance_per_hour", raised.exception.message_dict)

    def test_zero_maintenance_is_valid(self):
        self.machine.maintenance_per_hour = Decimal("0.00")

        self.machine.full_clean()

        self.assertEqual(self.machine.machine_cost_per_hour, Decimal("0.80"))
