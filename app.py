# --------------------------------------------- #
# Dashboard Imobiliário em Streamlit
# Feito para visualizar distribuições de probabilidade
# Autor: Bruna Petito (2025)
# --------------------------------------------- #

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import binom, poisson
import pathlib

# ----------------------------- #
# Configuração inicial da página
# ----------------------------- #
st.set_page_config(page_title="Dashboard Imobiliário", layout="wide")

# Carregar CSS externo (style.css) para deixar o código mais limpo
css_path = pathlib.Path("style.css")
if css_path.exists():
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ----------------------------- #
# Função auxiliar para criar KPIs
# (caixinhas que mostram valores de destaque)
# ----------------------------- #
def kpi(label, value):
    st.markdown(f"""
    <div class="kpi">
      <div class="label">{label}</div>
      <div class="value">{value}</div>
    </div>
    """, unsafe_allow_html=True)

# ----------------------------- #
# Título principal do dashboard
# ----------------------------- #
st.markdown(
    "<h1><span class='house'>🏠</span>Dashboard de Distribuições de Probabilidade - Imobiliária</h1>",
    unsafe_allow_html=True
)

# ----------------------------- #
# Criação das abas principais
# ----------------------------- #
tab1, tab2, tab3, tab4 = st.tabs(
    ["📖 Tutorial", "📌 Vendas por Visitas", "📞 Contatos por Dia", "🏡 Vendas por Mês"]
)

# ----------------------------- #
# Aba 1 - Tutorial
# ----------------------------- #
with tab1:
    st.header("📖 Como usar este Dashboard")
    st.markdown("""
    Este painel foi criado para **donos de imobiliárias** que querem ter uma visão **simples e prática** sobre os números do negócio.

    ### O que você pode fazer aqui:
    - **📌 Vendas por Visitas** → Descobrir quantos contratos pode esperar fechar a partir das visitas realizadas.  
    - **📞 Contatos por Dia** → Ver quantos clientes costumam entrar em contato diariamente.  
    - **🏡 Vendas por Mês** → Registrar a quantidade de imóveis vendidos por mês e as chances de cada cenário.  

    ### Como funciona:
    1. Ajuste os **controles (sliders e caixas de texto)** de acordo com os dados da sua imobiliária.  
    2. Veja o **gráfico central** mostrando a chance de cada resultado.  
    3. Acompanhe os **indicadores (média, variância e desvio padrão)** que resumem os números.  
    4. Leia a **explicação em destaque** logo abaixo de cada gráfico, que traduz os cálculos em linguagem simples.  
    """)

# ----------------------------- #
# Aba 2 - Vendas por Visitas (Distribuição Binomial)
# ----------------------------- #
with tab2:
    st.header("📌 Simulação de Vendas a partir das Visitas")
    st.write("Aqui dá para estimar **quantos contratos pode fechar** dependendo do número de visitas e da taxa de conversão.")

    with st.container():
        st.markdown('<div class="block">', unsafe_allow_html=True)

        # Entradas do usuário
        col_in1, col_in2 = st.columns([1,1])
        with col_in1:
            n = st.slider("Quantidade de visitas realizadas", 1, 50, 10)
        with col_in2:
            p = st.slider("Chance de fechar contrato por visita (%)", 0, 100, 30, step=1) / 100

        # Distribuição binomial
        x = np.arange(0, n+1)
        y = binom.pmf(x, n, p)

        # Gráfico
        fig, ax = plt.subplots()
        ax.bar(x, y, color="#8e66c6")
        ax.set_xlabel("Número de contratos fechados")
        ax.set_ylabel("Probabilidade")
        ax.set_title("Distribuição dos contratos")
        fig.set_size_inches(5, 3)

        # Centralizando o gráfico
        col_left, col_center, col_right = st.columns([1,2,1])
        with col_center:
            st.pyplot(fig)

        # Indicadores (KPIs)
        col1, col2, col3 = st.columns(3)
        with col1: kpi("Média esperada", f"{n*p:.2f}")
        with col2: kpi("Variância", f"{n*p*(1-p):.2f}")
        with col3: kpi("Desvio Padrão", f"{np.sqrt(n*p*(1-p)):.2f}")

        # Explicação amigável
        st.info(
            f"👉 Com **{n} visitas** e **{int(p*100)}% de chance de conversão por visita**, "
            f"você pode esperar em média **{n*p:.1f} contratos fechados**."
        )

        st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------- #
# Aba 3 - Contatos por Dia (Distribuição de Poisson)
# ----------------------------- #
with tab3:
    st.header("📞 Previsão de Contatos de Clientes por Dia")
    st.write("Aqui dá para prever **quantos clientes vão entrar em contato** em um dia comum.")

    with st.container():
        st.markdown('<div class="block">', unsafe_allow_html=True)

        # Entrada do usuário
        lmbda = st.slider("Média de contatos por dia", 1, 20, 5)

        # Distribuição de Poisson
        x = np.arange(0, lmbda*3)
        y = poisson.pmf(x, lmbda)

        # Gráfico
        fig, ax = plt.subplots()
        ax.bar(x, y, color="#b085f5")
        ax.set_xlabel("Número de contatos")
        ax.set_ylabel("Probabilidade")
        ax.set_title("Distribuição dos contatos diários")
        fig.set_size_inches(5, 3)

        # Centralizando o gráfico
        col_left, col_center, col_right = st.columns([1,2,1])
        with col_center:
            st.pyplot(fig)

        # Indicadores (KPIs)
        col1, col2, col3 = st.columns(3)
        with col1: kpi("Média esperada", f"{lmbda:.2f}")
        with col2: kpi("Variância", f"{lmbda:.2f}")
        with col3: kpi("Desvio Padrão", f"{np.sqrt(lmbda):.2f}")

        # Explicação amigável
        st.info(
            f"👉 Se em média **{lmbda} clientes** entram em contato por dia, "
            f"este gráfico mostra a chance de receber mais ou menos contatos."
        )

        st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------- #
# Aba 4 - Vendas por Mês (VA Discreta)
# ----------------------------- #
with tab4:
    st.header("🏡 Vendas por Mês")
    st.write("Aqui você pode registrar **quantos imóveis costuma vender por mês** e visualizar a chance de cada cenário.")

    with st.container():
        st.markdown('<div class="block">', unsafe_allow_html=True)

        # Entrada do usuário
        col_in1, col_in2 = st.columns([1,1])
        with col_in1:
            valores = st.text_input("Valores possíveis de vendas", "0,1,2,3,4,5")
        with col_in2:
            probs = st.text_input("Probabilidades correspondentes", "0.1,0.2,0.3,0.2,0.15,0.05")

        try:
            # Conversão dos dados
            valores = [int(v.strip()) for v in valores.split(",")]
            probs = [float(p.strip()) for p in probs.split(",")]

            # Verifica se as probabilidades somam 1
            if abs(sum(probs) - 1) > 0.001:
                st.error("As probabilidades devem somar 1 (100%).")
            else:
                # Gráfico
                fig, ax = plt.subplots()
                ax.bar(valores, probs, color="#d0bdf4")
                ax.set_xlabel("Número de imóveis vendidos")
                ax.set_ylabel("Probabilidade")
                ax.set_title("Distribuição das vendas mensais")
                fig.set_size_inches(5, 3)

                # Centralizando o gráfico
                col_left, col_center, col_right = st.columns([1,2,1])
                with col_center:
                    st.pyplot(fig)

                # Cálculos estatísticos
                media = np.sum([v*p for v, p in zip(valores, probs)])
                variancia = np.sum([((v - media)**2)*p for v, p in zip(valores, probs)])
                desvio = np.sqrt(variancia)

                # KPIs
                col1, col2, col3 = st.columns(3)
                with col1: kpi("Média esperada", f"{media:.2f}")
                with col2: kpi("Variância", f"{variancia:.2f}")
                with col3: kpi("Desvio Padrão", f"{desvio:.2f}")

                # Explicação amigável
                st.info(
                    f"👉 Em média, sua imobiliária pode esperar vender **{media:.1f} imóveis por mês**."
                )
        except:
            st.warning("Digite valores válidos para vendas e probabilidades.")

        st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------- #
# Rodapé
# ----------------------------- #
st.markdown("---")
st.caption("Feito com ❤️ em Streamlit • Petito Imóveis • © 2025")
