from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase

from .models import Marketplace


class MarketplaceValidationTests(TestCase):
    def make_marketplace(self, **overrides):
        data = {
            "nome": "Shopee (CPF)",
            "porcentagem_comissao": Decimal("14.00"),
            "taxa_fixa": Decimal("7.00"),
        }
        data.update(overrides)
        return Marketplace(**data)

    def assert_invalid(self, marketplace, field):
        with self.assertRaises(ValidationError) as raised:
            marketplace.full_clean()
        self.assertIn(field, raised.exception.message_dict)

    def test_valid_marketplace_passes_validation(self):
        self.make_marketplace().full_clean()

    def test_maximum_commission_passes_validation(self):
        self.make_marketplace(porcentagem_comissao=Decimal("99.99")).full_clean()

    def test_direct_sale_with_no_fees_passes_validation(self):
        self.make_marketplace(
            nome="Venda direta", porcentagem_comissao=Decimal("0.00"), taxa_fixa=Decimal("0.00")
        ).full_clean()

    def test_commission_of_100_fails_validation(self):
        self.assert_invalid(self.make_marketplace(porcentagem_comissao=Decimal("100")), "porcentagem_comissao")

    def test_negative_commission_fails_validation(self):
        self.assert_invalid(self.make_marketplace(porcentagem_comissao=Decimal("-1")), "porcentagem_comissao")

    def test_negative_fixed_fee_fails_validation(self):
        self.assert_invalid(self.make_marketplace(taxa_fixa=Decimal("-0.01")), "taxa_fixa")

    def test_blank_name_fails_validation(self):
        self.assert_invalid(self.make_marketplace(nome=""), "nome")

    def test_duplicate_name_fails_validation(self):
        self.make_marketplace().save()
        self.assert_invalid(self.make_marketplace(), "nome")

    def test_sale_price_grosses_up_net_target(self):
        marketplace = self.make_marketplace(porcentagem_comissao=Decimal("10.00"), taxa_fixa=Decimal("2.00"))
        self.assertEqual(marketplace.valor_venda(Decimal("100.00")), Decimal("113.33"))

    def test_sale_price_with_20_percent_commission_and_fixed_fee(self):
        marketplace = self.make_marketplace(
            porcentagem_comissao=Decimal("20.00"), taxa_fixa=Decimal("7.00")
        )

        self.assertEqual(marketplace.valor_venda(Decimal("93.00")), Decimal("125.00"))

    def test_sale_price_with_14_percent_commission(self):
        marketplace = self.make_marketplace()

        self.assertEqual(marketplace.valor_venda(Decimal("57.14")), Decimal("74.58"))

    def test_sale_price_half_cent_rounds_up(self):
        marketplace = self.make_marketplace(
            porcentagem_comissao=Decimal("20.00"), taxa_fixa=Decimal("7.00")
        )

        self.assertEqual(marketplace.valor_venda(Decimal("57.14")), Decimal("80.18"))

    def test_sale_price_57_10_rounds_to_80_13(self):
        marketplace = self.make_marketplace(
            porcentagem_comissao=Decimal("20.00"), taxa_fixa=Decimal("7.00")
        )

        self.assertEqual(marketplace.valor_venda(Decimal("57.10")), Decimal("80.13"))

    def test_direct_sale_returns_net_target(self):
        marketplace = self.make_marketplace(
            porcentagem_comissao=Decimal("0.00"), taxa_fixa=Decimal("0.00")
        )

        self.assertEqual(marketplace.valor_venda(Decimal("57.14")), Decimal("57.14"))
