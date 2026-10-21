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