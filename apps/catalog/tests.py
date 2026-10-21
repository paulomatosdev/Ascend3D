from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase

from .models import Material


class MaterialTests(TestCase):
    def make_material(self, **overrides):
        data = {
            "name": "PLA de teste",
            "material_type": Material.MaterialType.PLA,
            "spool_price": Decimal("120.00"),
            "spool_weight_g": 1000,
        }
        data.update(overrides)
        return Material(**data)

    def test_price_per_gram_is_calculated(self):
        material = self.make_material()

        self.assertEqual(material.price_per_gram, Decimal("0.12"))

    def test_zero_spool_weight_fails_validation(self):
        material = self.make_material(spool_weight_g=0)

        with self.assertRaises(ValidationError) as raised:
            material.full_clean()

        self.assertIn("spool_weight_g", raised.exception.message_dict)

    def test_non_positive_spool_price_fails_validation(self):
        for price in (Decimal("0.00"), Decimal("-0.01")):
            with self.subTest(price=price):
                material = self.make_material(spool_price=price)

                with self.assertRaises(ValidationError) as raised:
                    material.full_clean()

                self.assertIn("spool_price", raised.exception.message_dict)
