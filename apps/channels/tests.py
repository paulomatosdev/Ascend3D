from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase

from .models import SalesChannel


class SalesChannelValidationTests(TestCase):
    def make_channel(self, **overrides):
        data = {
            "name": "Shopee (CPF)",
            "commission_percent": Decimal("14.00"),
            "fixed_fee": Decimal("7.00"),
        }
        data.update(overrides)
        return SalesChannel(**data)

    def assert_invalid(self, channel, field):
        with self.assertRaises(ValidationError) as raised:
            channel.full_clean()

        self.assertIn(field, raised.exception.message_dict)

    def test_valid_channel_passes_validation(self):
        self.make_channel().full_clean()

    def test_maximum_commission_passes_validation(self):
        self.make_channel(commission_percent=Decimal("99.99")).full_clean()

    def test_direct_sale_with_no_fees_passes_validation(self):
        channel = self.make_channel(
            name="Venda direta",
            commission_percent=Decimal("0.00"),
            fixed_fee=Decimal("0.00"),
        )

        channel.full_clean()

    def test_commission_of_100_fails_validation(self):
        channel = self.make_channel(commission_percent=Decimal("100"))

        self.assert_invalid(channel, "commission_percent")

    def test_negative_commission_fails_validation(self):
        channel = self.make_channel(commission_percent=Decimal("-1"))

        self.assert_invalid(channel, "commission_percent")

    def test_commission_with_three_decimal_places_fails_validation(self):
        channel = self.make_channel(commission_percent=Decimal("14.555"))

        self.assert_invalid(channel, "commission_percent")

    def test_negative_fixed_fee_fails_validation(self):
        channel = self.make_channel(fixed_fee=Decimal("-0.01"))

        self.assert_invalid(channel, "fixed_fee")

    def test_blank_name_fails_validation(self):
        channel = self.make_channel(name="")

        self.assert_invalid(channel, "name")

    def test_duplicate_name_fails_validation(self):
        self.make_channel().save()

        self.assert_invalid(self.make_channel(), "name")