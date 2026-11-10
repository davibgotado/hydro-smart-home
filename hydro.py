from datetime import datetime

class HydroBubbleEngine:
    def __init__(self, meta_diaria_litros: float = 150.0, preco_m3: float = 6.50):
        """
        Motor de inteligência computacional do Hydro integrado ao Bubble.io.
        :param meta_diaria_litros: Meta configurada no perfil do User no Bubble.
        :param preco_m3: Tarifa de água por m³ (padrão R$ 6,50).
        """
        self.meta_diaria = meta_diaria_litros
        self.preco_m3 = preco_m3

    def processar_leituras_bubble(self, registros_bubble: list[dict]) -> dict:
        """
        Recebe a lista de objetos 'Leitura_Agua' vinda do Bubble.io.
        """
        if not registros_bubble:
            return {"status": "SEM_DADOS", "total_litros": 0.0, "alertas": []}

        # Calculando o consumo total acumulado no dia
        total_litros = sum(item["volume_litros"] for item in registros_bubble)
        alertas = []

        # Regra 1: Validação de estouro da meta diária do usuário
        if total_litros > self.meta_diaria:
            excesso = total_litros - self.meta_diaria
            alertas.append({
                "tipo": "META_EXCEDIDA",
                "prioridade": "ALTA",
                "mensagem": f"Meta ultrapassada em {excesso:.1f} L! Limite cadastrado: {self.meta_diaria} L."
            })

        # Regra 2: Algoritmo de identificação de pico anormal / potencial vazamento (>= 80L num evento)
        picos = [item for item in registros_bubble if item["volume_litros"] >= 80.0]
        if picos:
            for pico in picos:
                alertas.append({
                    "tipo": "POSSIVEL_VAZAMENTO",
                    "prioridade": "CRÍTICA",
                    "mensagem": f"Fluxo atípico de {pico['volume_litros']} L registrado no cômodo '{pico['comodo']}' às {pico['hora']}."
                })

        # Regra 3: Cálculo financeiro em R$ (Conversão de Litros para Metros Cúbicos)
        custo_estimado = (total_litros / 1000.0) * self.preco_m3

        return {
            "data_processamento": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "total_litros": round(total_litros, 2),
            "meta_diaria": self.meta_diaria,
            "percentual_meta": round((total_litros / self.meta_diaria) * 100, 1),
            "custo_estimado_brl": round(custo_estimado, 2),
            "total_registros": len(registros_bubble),
            "alertas": alertas
        }


# --- SIMULAÇÃO DE LEITURAS REGISTRADAS NO BUBBLE ---
if __name__ == "__main__":
    print("======================================================")
    print("   HYDRO ENGINE - INTEGRAÇÃO BUBBLE (EXPOTECH 2050)   ")
    print("======================================================")

    # Dados idênticos aos que são gravados pela sua tela do Bubble
    dados_recebidos_do_bubble = [
        {"hora": "07:30", "volume_litros": 20.0, "comodo": "Banheiro"},
        {"hora": "12:15", "volume_litros": 15.5, "comodo": "Cozinha"},
        {"hora": "16:40", "volume_litros": 85.0, "comodo": "Lavanderia"},  # Trigger de pico/vazamento
        {"hora": "19:00", "volume_litros": 25.0, "comodo": "Banheiro"}
    ]

    # Processando os dados para um usuário com meta de 120 Litros
    engine = HydroBubbleEngine(meta_diaria_litros=120.0)
    relatorio = engine.processar_leituras_bubble(dados_recebidos_do_bubble)

    # Exibição dos resultados no terminal
    print(f"\nData da Análise: {relatorio['data_processamento']}")
    print(f"Registros Processados: {relatorio['total_registros']}")
    print(f"Volume Acumulado: {relatorio['total_litros']} L / {relatorio['meta_diaria']} L ({relatorio['percentual_meta']}% da meta)")
    print(f"Custo Estimado no Dia: R$ {relatorio['custo_estimado_brl']}")

    if relatorio['alertas']:
        print("\n[ALERTAS DE SISTEMA DISPARADOS]")
        for a in relatorio['alertas']:
            print(f"  • [{a['prioridade']}] {a['tipo']}: {a['mensagem']}")
    else:
        print("\n[STATUS] Consumo dentro da normalidade.")