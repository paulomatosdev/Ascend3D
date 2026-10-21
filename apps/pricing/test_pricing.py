from decimal import Decimal

from django.test import SimpleTestCase

from apps.catalog.models import Material

from .service import calcular_custo_material


class CustoMaterialTests(SimpleTestCase):
    def test_custo(self):
        # 1) Preparar: um material de verdade, só na memória (sem salvar)
        material = Material(
            name="PLA Preto",
            material_type=Material.MaterialType.PLA,
            spool_price=Decimal("120.00"),
            spool_weight_g=1000,
        )

        # 2) Agir: chamar a função que estamos testando
        resultado = calcular_custo_material(Decimal("100"), material)

        # 3) Conferir: o resultado é o que esperamos?
        self.assertEqual(resultado, Decimal("13.20"))