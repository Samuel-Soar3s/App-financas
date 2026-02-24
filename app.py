import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import numpy as np

st.set_page_config(
    page_title="Controle Financeiro",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Controle Financeiro Pessoal")

# Base em memória
if "dados" not in st.session_state:
    st.session_state.dados = pd.DataFrame(
        columns=["Data","Categoria","Tipo","Valor"]
    )

categorias = {
    "Educação":"Necessidade",
    "Alimentação":"Necessidade",
    "Energia":"Necessidade",
    "Água":"Necessidade",
    "Internet":"Necessidade",
    "Telefone":"Necessidade",
    "Cartão 1":"Desejo",
    "Cartão 2":"Desejo",
    "Cartão 3":"Desejo",
    "Investimento":"Poupança",
    "Poupança Filho":"Poupança"
}

menu = st.sidebar.radio(
    "Menu",
    ["Lançamentos","Cartões","Dashboard","Investimentos"]
)

# ---------------- Lançamentos ----------------
if menu == "Lançamentos":
    st.subheader("Novo Lançamento")

    data = st.date_input("Data", datetime.today())
    categoria = st.selectbox("Categoria", list(categorias.keys()))
    valor = st.number_input("Valor", min_value=0.0)

    if st.button("Salvar"):
        tipo = categorias[categoria]
        novo = pd.DataFrame(
            [[data,categoria,tipo,valor]],
            columns=["Data","Categoria","Tipo","Valor"]
        )
        st.session_state.dados = pd.concat(
            [st.session_state.dados,novo],
            ignore_index=True
        )
        st.success("Lançamento salvo com sucesso")

    st.dataframe(st.session_state.dados)

# ---------------- Cartões ----------------
if menu == "Cartões":
    st.subheader("Compra Parcelada")

    data = st.date_input("Data da Compra", datetime.today())
    cartao = st.selectbox("Cartão",["Cartão 1","Cartão 2","Cartão 3"])
    valor = st.number_input("Valor Total", min_value=0.0)
    parcelas = st.number_input("Parcelas", min_value=1, step=1)

    if st.button("Gerar Parcelas"):
        valor_parcela = valor/parcelas
        for i in range(parcelas):
            nova_data = pd.to_datetime(data) + pd.DateOffset(months=i)
            tipo = categorias[cartao]
            novo = pd.DataFrame(
                [[nova_data,cartao,tipo,valor_parcela]],
                columns=["Data","Categoria","Tipo","Valor"]
            )
            st.session_state.dados = pd.concat(
                [st.session_state.dados,novo],
                ignore_index=True
            )
        st.success("Parcelas geradas automaticamente")

# ---------------- Dashboard ----------------
if menu == "Dashboard":
    st.subheader("Resumo Financeiro")

    if not st.session_state.dados.empty:
        df = st.session_state.dados.copy()
        df["Mes"] = pd.to_datetime(df["Data"]).dt.to_period("M")

        resumo = df.groupby("Tipo")["Valor"].sum().reset_index()

        fig = px.pie(
            resumo,
            values="Valor",
            names="Tipo",
            title="Distribuição Financeira"
        )
        st.plotly_chart(fig, use_container_width=True)

        mensal = df.groupby("Mes")["Valor"].sum().reset_index()

        fig2 = px.line(
            mensal,
            x="Mes",
            y="Valor",
            title="Evolução Mensal"
        )
        st.plotly_chart(fig2, use_container_width=True)

    else:
        st.info("Ainda não há lançamentos registrados.")

# ---------------- Investimentos ----------------
if menu == "Investimentos":
    st.subheader("Simulador de Juros Compostos")

    inicial = st.number_input("Valor Inicial", min_value=0.0)
    aporte = st.number_input("Aporte Mensal", min_value=0.0)
    taxa = st.number_input("Taxa Mensal (%)", min_value=0.0)
    meses = st.number_input("Meses", min_value=1, step=1)

    if st.button("Simular"):
        valores = []
        saldo = inicial

        for i in range(meses):
            saldo = saldo*(1+taxa/100) + aporte
            valores.append(saldo)

        df_sim = pd.DataFrame({
            "Mes": range(1,meses+1),
            "Saldo": valores
        })

        fig = px.line(
            df_sim,
            x="Mes",
            y="Saldo",
            title="Projeção de Crescimento"
        )
        st.plotly_chart(fig, use_container_width=True)
import streamlit as st
st.title("App Teste")
st.write("Se você está vendo isso, funcionou.")
