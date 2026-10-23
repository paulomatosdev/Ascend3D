from decimal import Decimal

from django.test import SimpleTestCase

from apps.catalog.models import Material
from apps.machines.models import Maquina

from .models import PerfilPrecificacao

from .service import (
    aplicar_taxa_falha,
    calcular_custo_energia,
    calcular_custo_mao_de_obra,
    calcular_custo_maquina,
    calcular_custo_material,
    calcular_custo_total,
)


class PrecificacaoTestCase(SimpleTestCase):
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
            markup=Decimal("100.00"),
        )
        self.material = material
        self.maquina = maquina
        self.perfil = perfil


class CustoMaterialTests(PrecificacaoTestCase):
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


class CustoEnergiaTests(PrecificacaoTestCase):
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


class CustoMaquinaTests(PrecificacaoTestCase):
    def test_custo_de_maquina_para_cinco_horas(self):
        resultado = calcular_custo_maquina(self.maquina, Decimal("5"))

        self.assertEqual(resultado, Decimal("5.50"))

    def test_zero_horas_de_maquina_custa_zero(self):
        resultado = calcular_custo_maquina(self.maquina, Decimal("0"))

        self.assertEqual(resultado, Decimal("0"))

    def test_horas_negativas_geram_erro_no_custo_de_maquina(self):
        with self.assertRaises(ValueError):
            calcular_custo_maquina(self.maquina, Decimal("-1"))


class CustoMaoDeObraTests(PrecificacaoTestCase):
    def test_custo_de_mao_de_obra_para_quinze_minutos(self):
        resultado = calcular_custo_mao_de_obra(self.perfil, Decimal("15"))

        self.assertEqual(resultado, Decimal("5"))

    def test_zero_minutos_de_trabalho_custa_zero(self):
        resultado = calcular_custo_mao_de_obra(self.perfil, Decimal("0"))

        self.assertEqual(resultado, Decimal("0"))

    def test_minutos_negativos_geram_erro_no_custo_de_mao_de_obra(self):
        with self.assertRaises(ValueError):
            calcular_custo_mao_de_obra(self.perfil, Decimal("-1"))


class AplicarTaxaFalhaTests(PrecificacaoTestCase):
    def test_taxa_de_falha_dez_porcento_divide_o_custo_base(self):
        custo_base = Decimal("19.4125")

        resultado = aplicar_taxa_falha(custo_base, self.perfil)

        self.assertAlmostEqual(resultado, Decimal("21.5694"), places=4)
        self.assertGreater(resultado, custo_base)

    def test_taxa_de_falha_zero_preserva_o_custo_base(self):
        self.perfil.porcentagem_falha = Decimal("0.00")

        resultado = aplicar_taxa_falha(Decimal("19.4125"), self.perfil)

        self.assertEqual(resultado, Decimal("19.4125"))

    def test_custo_base_negativo_informa_que_o_custo_base_nao_pode_ser_negativo(self):
        with self.assertRaisesMessage(ValueError, "O custo base não pode ser negativo."):
            aplicar_taxa_falha(Decimal("-1"), self.perfil)

    def test_taxa_de_falha_de_cem_porcento_gera_erro(self):
        self.perfil.porcentagem_falha = Decimal("100.00")

        with self.assertRaisesMessage(
            ValueError,
            "A taxa de falha deve ser maior ou igual a zero e menor que 100%.",
        ):
            aplicar_taxa_falha(Decimal("10.00"), self.perfil)


class CustoTotalTests(PrecificacaoTestCase):
    def test_custo_total_do_exemplo_do_guia(self):
        resultado = calcular_custo_total(
            self.material,
            Decimal("100"),
            self.maquina,
            self.perfil,
            Decimal("5"),
            Decimal("15"),
        )

        self.assertAlmostEqual(resultado, Decimal("28.5694"), places=4)
        self.assertAlmostEqual(resultado, Decimal("28.57"), places=2)

    def test_custo_total_com_todos_os_consumos_zero_inclui_embalagem(self):
        resultado = calcular_custo_total(
            self.material,
            Decimal("0"),
            self.maquina,
            self.perfil,
            Decimal("0"),
            Decimal("0"),
        )

        self.assertEqual(resultado, Decimal("2.00"))
