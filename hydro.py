
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
