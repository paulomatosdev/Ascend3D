# Ascend

Sistema para ajudar quem está começando na impressão 3D a **precificar suas peças** com segurança, camada por camada: do custo real de produção até o preço final de venda.

> Status: em planejamento. Backend em Django.

## O problema

Quem começa a imprimir em 3D costuma cobrar só o filamento (ou "3 vezes o filamento") e acaba vendendo no prejuízo, porque esquece energia, desgaste da máquina, mão de obra, falhas, embalagem, impostos e taxas do marketplace.

## A ideia

O Ascend calcula o preço de uma peça somando cada camada de custo e aplicando margem e taxas de venda. O usuário evolui por níveis, começando simples e desbloqueando o restante conforme aprende:

| Nível | Nome | O que cobre |
| --- | --- | --- |
| 1 | Base | Material e energia |
| 2 | Estrutura | Máquina (depreciação e manutenção), mão de obra e falhas |
| 3 | Venda | Impostos, taxas de marketplace e margem |
| 4 | Escala | Pedido mínimo, taxa de setup, preço por complexidade e histórico de orçamentos |

## Fórmulas

```
Material      = gramas / 1000 * preço_por_kg * 1,10          (10% de folga para purga e suportes)
Energia       = horas * kW_médios * tarifa_kWh
Máquina/hora  = (preço_compra - valor_revenda) / horas_vida_útil + manutenção_por_hora
Máquina       = horas * Máquina/hora

Custo   = (Material + Energia + Máquina) / (1 - taxa_falha) + Mão_de_obra + Embalagem
Preço   = (Custo * (1 + markup) + taxa_fixa_canal) / (1 - taxa_percentual_canal)

Margem  = markup / (1 + markup)
```

### Exemplo

Peça de 100 g, 5 horas, filamento a R$ 120/kg, impressora de R$ 3.000 (revenda R$ 600, 3.000 h de vida útil), 150 W médios, kWh a R$ 0,95, manutenção de R$ 0,30/h, 15 min de trabalho a R$ 20/h, falha de 10%, embalagem de R$ 2:

- Custo total: R$ 28,57
- Preço direto com markup de 100%: R$ 57,14
- Preço na Shopee (14% + R$ 7 fixos): R$ 74,58

Os valores são hipóteses de exemplo, não preços de mercado.

## Stack

- Python 3.12+
- Django
- Banco de dados: SQLite no desenvolvimento (PostgreSQL em produção, a definir)

## Estrutura sugerida

```
ascend/
├── config/            # settings, urls, wsgi/asgi
├── apps/
│   ├── accounts/      # usuários e autenticação
│   ├── catalog/       # materiais (filamento, resina) e preço por grama
│   ├── machines/      # impressoras, depreciação, manutenção e consumíveis
│   ├── pricing/       # motor de cálculo de custo e preço
│   ├── channels/      # canais de venda e taxas (Shopee, Mercado Livre, venda direta)
│   └── quotes/        # orçamentos e histórico
├── manage.py
└── requirements.txt
```

## Modelos principais (rascunho)

- `Material`: nome, tipo, preço do rolo, peso do rolo (preço por grama calculado).
- `Printer`: nome, tecnologia (FDM ou resina), preço de compra, valor de revenda, horas de vida útil, potência média em watts, manutenção por hora.
- `SalesChannel`: nome, comissão percentual, taxa fixa por item.
- `PricingProfile`: tarifa do kWh, valor da hora de trabalho, taxa de falha, embalagem padrão, markup padrão.
- `Quote`: peça, gramas, horas de impressão, tempo de trabalho, canal, custo calculado, preço sugerido.

## Como rodar localmente

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install django
django-admin startproject config .
python manage.py migrate
python manage.py runserver
```

Depois de criar o projeto, registre os apps em `INSTALLED_APPS` e rode as migrações a cada mudança nos modelos:

```bash
python manage.py makemigrations
python manage.py migrate
```

## Roadmap

- [ ] Cadastro de materiais, impressoras e canais de venda
- [ ] Motor de cálculo de custo e preço (Níveis 1 a 3)
- [ ] Orçamento por peça com histórico (Nível 4)
- [ ] Testes automatizados das fórmulas
- [ ] Suporte a resina (FEP, tela LCD e álcool isopropílico por hora)
- [ ] Cálculo de custo a partir de dados do fatiador (peso e tempo)
- [ ] Autenticação e múltiplos usuários

## Observações sobre impostos e taxas

Limites do MEI e taxas de marketplace mudam com frequência. Mantenha esses valores configuráveis no sistema (não fixos no código) e confirme-os nas fontes oficiais. O enquadramento (MEI ou outro) e o CNAE devem ser validados com um contador.

## Documentação

O guia completo de precificação que embasa as fórmulas está no documento "Guia de precificação de impressão 3D para iniciantes".

## Licença

A definir.
