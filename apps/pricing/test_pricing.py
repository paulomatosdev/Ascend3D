from decimal import Decimal

from django.test import SimpleTestCase

from apps.catalog.models import Material
from apps.machines.models import Maquina

from .models import PerfilPrecificacao

from .service import calcular_custo_energia, calcular_custo_material


class CustoMaterialTests(SimpleTestCase):
    def setUp(self):
        material = Material(
            name="PLA Preto",
            material_type=Material.MaterialType.PLA,
            spool_price=Decimal("120.00"),
            spool_weight_g=1000,
        )
        maquina = Maquina(
            nome="Impressora de teste",
            tipo_impressao=Maquina.TipoImpressao.FDM,
            preco_compra=Decimal("3000.00"),
            valor_revenda=Decimal("600.00"),
            vida_util_horas=3000,
            consumo_watts=150,
            manutencao_por_hora=Decimal("0.30"),
        )
        perfil = PerfilPrecificacao(
            nome="Perfil de teste",
            tarifa_kwh=Decimal("0.95"),
            valor_hora_trabalhada=Decimal("20.00"),
            porcentagem_falha=Decimal("10.00"),
            custo_embalagem=Decimal("2.00"),
            markup=Decimal("10.00"),
        )
        self.material = material
        self.maquina = maquina
        self.perfil = perfil

    def test_zero_gramas_custa_zero(self):
        resultado = calcular_custo_material(Decimal("0"), self.material)

        self.assertEqual(resultado, Decimal("0"))

    def test_gramagem_negativa_gera_erro(self):
        with self.assertRaises(ValueError):
            calcular_custo_material(Decimal("-1"), self.material)

    def test_fator_desperdicio_nomeado_substitui_o_padrao(self):
        resultado = calcular_custo_material(
            Decimal("100"),
            self.material,
            fator_desperdicio=Decimal("1.00"),
        )

        self.assertEqual(resultado, Decimal("12.00"))

    def test_custo_padrao_de_100_gramas(self):
        resultado = calcular_custo_material(Decimal("100"), self.material)

        self.assertEqual(resultado, Decimal("13.20"))

    def test_custo_de_energia_para_150_watts_por_cinco_horas(self):
        resultado = calcular_custo_energia(self.maquina, self.perfil, Decimal("5"))

        self.assertEqual(resultado, Decimal("0.7125"))

    def test_zero_horas_de_energia_custa_zero(self):
        resultado = calcular_custo_energia(self.maquina, self.perfil, Decimal("0"))

        self.assertEqual(resultado, Decimal("0"))

    def test_horas_negativas_geram_erro_no_custo_de_energia(self):
        with self.assertRaises(ValueError):
            calcular_custo_energia(self.maquina, self.perfil, Decimal("-1"))

    def test_soma_de_material_e_energia_do_nivel_1(self):
        custo_material = calcular_custo_material(Decimal("100"), self.material)
        custo_energia = calcular_custo_energia(self.maquina, self.perfil, Decimal("5"))

        self.assertEqual(custo_material + custo_energia, Decimal("13.9125"))
