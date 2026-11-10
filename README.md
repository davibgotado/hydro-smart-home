# 🚰 Hydro - Gestão Inteligente de Água (Smart Home 2050)

> Projeto desenvolvido para a **ExpoTech 2026.2 - Missão 2050** (Categoria START).

---

## 📌 1. Product Management

### Contexto & Problema
Em 2050, a gestão sustentável de recursos hídricos em casas inteligentes é fundamental. O consumo invisível de água e pequenos vazamentos não detectados geram grande desperdício financeiro e impacto ambiental.

### Público-Alvo & Persona
* **Persona:** Lucas, 30 anos, morador de uma Smart Home focada em eficiência energética e sustentabilidade. Deseja acompanhar o consumo de água em tempo real, prever gastos e evitar surpresas na conta do mês.

### MVP (Minimum Viable Product)
* **Registro de Consumo:** Inserção do volume de água consumido por cômodo da casa.
* **Dashboard Visual:** Acompanhamento do progresso em relação à meta diária estabelecida.
* **Motor Computacional:** Algoritmo em Python para validação de limites, cálculo de custos em R$ e detecção automática de anomalias (vazamentos).

### Priorização de Backlog (Matriz MoSCoW)
* **Must Have:** Cadastro de leituras de água, cálculo de total acumulado do dia, indicador de estouro de meta.
* **Should Have:** Detecção algorítmica de picos repentinos de consumo (vazamento), dashboard no-code responsivo.
* **Could Have:** Notificações automáticas via Make/n8n disparadas para o celular do morador.
* **Won't Have (nesta versão):** Integração física com sensores IoT via hardware em tempo real.

---

## 🛠️ 2. No-Code Development Platforms (Bubble.io)

O aplicativo **Hydro** foi construído na plataforma no-code **Bubble.io** (`https://hydro-91774.bubbleapps.io/version-test`).

* **Modelagem de Dados Visual (Data Types):**
  * `User`: Guarda as credenciais do morador e a sua `meta_diaria` em litros.
  * `Leitura_Agua`: Armazena cada evento de uso, contendo `volume_litros`, `comodo`, `data_hora` e o vínculo com o `User`.
* **Interface & Autenticação:**
  * Fluxo nativo de Sign Up / Log In de utilizador.
  * Formulário responsivo com campo numérico e *dropdown* para seleção de cômodos.
  * Painel de monitoramento do progresso acumulado.

---

## 🐍 3. Computational Logic Using Python

O script `hydro.py` funciona como o motor de inteligência do produto, aplicando as seguintes regras de negócio:

1. **Conversão Financeira:** Calcula o valor acumulado em R$ com base no consumo em metros cúbicos ($m^3$).
2. **Validação de Meta:** Compara o volume total do dia com o limite cadastrado pelo morador.
3. **Algoritmo de Detecção de Anomalias:** Identifica fluxos atípicos num único evento ($\ge 80\text{L}$), emitindo alerta de prioridade crítica para prevenção de vazamentos.

### Como executar o código:
```bash
python hydro.py