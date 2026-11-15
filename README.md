# 💧 Hydro — Sistema Inteligente de Monitoramento de Água

Turma: CDC Noturno — 1º Semestre

##  Integrantes do Grupo
* Gustavo Henrique Macedo Marques — RA 284579 (Líder)
* Sofia Camacho — RA 284192
* Davi Barros Gotado — RA 295153
* Amanda Maria de Sousa Gabriel — RA 275780

---

##  Visão Geral do Projeto

* **O Problema:** Falta de visibilidade sobre o consumo residencial de água e diagnóstico tardio de vazamentos. Na maioria das residências, anomalias só são descobertas semanas depois na fatura mensal, gerando prejuízo financeiro e desperdício ambiental.
* **A Persona:** Morador ou gestor residencial consciente que busca controlar gastos, evitar danos estruturais por vazamentos e acompanhar o consumo diário de forma simples e visual.
* **A Solução (Hydro):** Plataforma modular de monitoramento inteligente que integra interface **No-Code (Bubble)**, API REST em **Python (FastAPI)** para cálculo de cotas e detecção de anomalias, e automação **Low-Code (Make / n8n)** para disparo de alertas em tempo real por e-mail.
* **Ganho de Eficiência:** Reduz o tempo de resposta a vazamentos e estouros de consumo de **semanas para segundos**.

---

##  Arquitetura do Sistema

### 1. Front-End & Banco de Dados No-Code (Bubble)
Desenvolvido para oferecer transparência e gestão diária ao morador:
* **Painel Principal (`/painel`):** Dashboard com total consumido, acompanhamento da meta diária e registro setorizado por cômodo (Cozinha, Lavanderia, Banheiro).
* **Histórico (`/historico`):** Consulta dinâmica ordenada por data e cômodo para análise de tendências e auditoria de alertas.
* **Estrutura do Banco de Dados:**
  * `User`: Armazena nome, e-mail e meta diária do usuário.
  * `Leitura_Agua`: Registra volume em litros, cômodo, data/hora e vínculo com o usuário.
* **Link da Aplicação:** [Acessar Hydro no Bubble](https://hydro-91774.bubbleapps.io/version-test/painel)

---

### 2. Back-End & Regras de Negócio (Python + FastAPI)
O arquivo `hydro.py` implementa uma API RESTful responsável pelo processamento matemático e validação das regras de segurança:
* **Cota Per Capita (`200L/pessoa`):** Calcula o consumo médio individual (`consumo_diario / numero_pessoas`) e ativa `alerta_cota` caso ultrapasse 200 litros por morador.
* **Detecção de Vazamento (`700L/dia`):** Avalia o volume total diário e ativa `alerta_vazamento` caso ultrapasse 700 litros.

#### Código-Fonte (`hydro.py`)
```python
from fastapi import FastAPI

app = FastAPI(
    title="Sistema de Monitoramento de Água"
)

COTA_POR_PESSOA = 200
LIMITE_ALERTA = 700


@app.get("/")
def inicio():
    return {
        "mensagem": "Sistema de Monitoramento de Água"
    }


@app.post("/consumo")
def calcular_consumo(
    consumo_diario: float,
    numero_pessoas: int
):
    if numero_pessoas <= 0 or consumo_diario < 0:
        return {
            "erro": "Valores inválidos"
        }

    consumo_por_pessoa = (
        consumo_diario / numero_pessoas
    )

    alerta_cota = (
        consumo_por_pessoa > COTA_POR_PESSOA
    )

    alerta_vazamento = (
        consumo_diario > LIMITE_ALERTA
    )

    return {
        "consumo_diario": consumo_diario,
        "numero_pessoas": numero_pessoas,
        "consumo_por_pessoa": round(
            consumo_por_pessoa, 2
        ),
        "cota_por_pessoa": COTA_POR_PESSOA,
        "alerta_cota": alerta_cota,
        "alerta_vazamento": alerta_vazamento
    }
