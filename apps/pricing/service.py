from decimal import Decimal

FATOR_DESPERDICIO = Decimal('1.10')

def calcular_custo_material(gramagem_total, material, fator_desperdicio=FATOR_DESPERDICIO):
    if gramagem_total < 0:
        raise ValueError("A gramagem total não pode ser negativa.")
    custo_material = gramagem_total * material.price_per_gram * fator_desperdicio
    return custo_material

def calcular_custo_energia(maquina, perfil, horas):
    if horas < 0:
        raise ValueError("O número de horas não pode ser negativo.")
    custo_energia = (maquina.consumo_watts / Decimal('1000')) * perfil.tarifa_kwh * horas
    return custo_energia


def calcular_custo_maquina(maquina, horas):
    if horas < 0:
        raise ValueError("O número de horas não pode ser negativo.")
    custo_maquina = maquina.maquina_custo_por_hora * horas
    return custo_maquina


def calcular_custo_mao_de_obra(perfil, minutos):
    if minutos < 0:
        raise ValueError("O número de minutos não pode ser negativo.")
    horas_trabalhadas = minutos / Decimal("60")
    custo_mao_de_obra = perfil.valor_hora_trabalhada * horas_trabalhadas
    return custo_mao_de_obra


def aplicar_taxa_falha(custo_base, perfil):
    if custo_base < 0:
        raise ValueError("O custo base não pode ser negativo.")
    taxa_falha = perfil.taxa_falha
    if taxa_falha < 0 or taxa_falha >= Decimal("1"):
        raise ValueError("A taxa de falha deve ser maior ou igual a zero e menor que 100%.")
    custo_ajustado = custo_base / (Decimal("1") - taxa_falha)
    return custo_ajustado


def calcular_custo_total(
    material,
    gramagem_total,
    maquina,
    perfil,
    horas_impressao,
    minutos_trabalho,
):
    custo_material = calcular_custo_material(gramagem_total, material)
    custo_energia = calcular_custo_energia(maquina, perfil, horas_impressao)
    custo_maquina = calcular_custo_maquina(maquina, horas_impressao)
    custo_base = custo_material + custo_energia + custo_maquina
    custo_base_ajustado = aplicar_taxa_falha(custo_base, perfil)
    custo_mao_de_obra = calcular_custo_mao_de_obra(perfil, minutos_trabalho)
    return custo_base_ajustado + custo_mao_de_obra + perfil.custo_embalagem
