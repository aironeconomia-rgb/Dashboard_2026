from pathlib import Path
from html import escape
from textwrap import dedent

import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


# =========================
# CONFIGURAÇÃO DA PÁGINA
# =========================

st.set_page_config(
    page_title="Dashboard Comercial de Vendas",
    page_icon="📊",
    layout="wide"
)


# =========================
# IDENTIDADE VISUAL DO DASHBOARD
# =========================

NOME_EMPRESA = "Empresa Comercial de Vendas"

SUBTITULO_DASHBOARD = (
    "Painel gerencial para acompanhamento de vendas, receita, lucro, produtos, "
    "canais comerciais e desempenho regional."
)

COR_FUNDO = "#F3F6FB"
COR_CARD = "#FFFFFF"
COR_TEXTO = "#0F172A"
COR_TEXTO_SECUNDARIO = "#334155"
COR_TEXTO_SUAVE = "#64748B"
COR_BORDA = "#D7E0EC"
COR_DESTAQUE = "#1F3A5F"
COR_DESTAQUE_2 = "#C99512"
COR_CRITICO = "#DC2626"
COR_POSITIVO = "#15803D"

LIMITE_MINIMO_META = 80
LIMITE_MAXIMO_ATRASO = 20
LIMITE_MINIMO_MARGEM = 10

CORES_GRAFICOS = [
    "#1F3A5F",
    "#D4A017",
    "#3E5C76",
    "#A23E48",
    "#2F855A",
    "#805AD5",
    "#C05621",
    "#2B6CB0"
]

px.defaults.template = "plotly_white"
px.defaults.color_discrete_sequence = CORES_GRAFICOS


# =========================
# ESTILO VISUAL
# =========================

def aplicar_estilo_dashboard():
    st.markdown(
        f"""
        <style>
            [data-testid="stSidebar"] {{
                display: none !important;
            }}

            [data-testid="stAppViewContainer"] {{
                background: {COR_FUNDO} !important;
            }}

            [data-testid="stHeader"] {{
                background: rgba(243, 246, 251, 0.96) !important;
                backdrop-filter: blur(8px);
            }}

            .block-container {{
                max-width: 1450px;
                padding-top: 1.4rem;
                padding-bottom: 3rem;
            }}

            h1, h2, h3, h4, h5, h6,
            [data-testid="stMarkdownContainer"] h1,
            [data-testid="stMarkdownContainer"] h2,
            [data-testid="stMarkdownContainer"] h3,
            [data-testid="stMarkdownContainer"] h4 {{
                color: {COR_TEXTO} !important;
                font-weight: 900 !important;
                letter-spacing: -0.02em;
            }}

            [data-testid="stMarkdownContainer"] p,
            p, label {{
                color: {COR_TEXTO_SECUNDARIO} !important;
                font-size: 1rem;
            }}

            .topo-dashboard {{
                background: linear-gradient(135deg, #FFFFFF 0%, #F4F8FF 60%, #FFF4D8 100%);
                border: 1px solid {COR_BORDA};
                border-radius: 24px;
                padding: 28px 32px;
                margin-bottom: 20px;
                box-shadow: 0 14px 34px rgba(15, 23, 42, 0.09);
            }}

            .topo-dashboard__tag {{
                color: {COR_DESTAQUE_2} !important;
                font-size: 0.86rem;
                font-weight: 900;
                letter-spacing: 0.10em;
                text-transform: uppercase;
                margin-bottom: 10px;
            }}

            .topo-dashboard__titulo {{
                color: {COR_TEXTO} !important;
                font-size: 2.3rem;
                font-weight: 950;
                line-height: 1.12;
                margin: 0;
            }}

            .topo-dashboard__subtitulo {{
                color: {COR_TEXTO_SECUNDARIO} !important;
                font-size: 1.04rem;
                font-weight: 600;
                max-width: 980px;
                margin-top: 12px;
                margin-bottom: 0;
            }}

            div[data-testid="stRadio"] > label {{
                font-size: 1rem !important;
                font-weight: 800 !important;
                color: {COR_TEXTO} !important;
            }}

            div[role="radiogroup"] {{
                background: {COR_CARD};
                border: 1px solid {COR_BORDA};
                border-radius: 18px;
                padding: 10px 14px;
                box-shadow: 0 8px 24px rgba(15, 23, 42, 0.05);
                margin-bottom: 24px;
            }}

            div[role="radiogroup"] label {{
                background: #F8FAFC;
                border: 1px solid #DCE5F1;
                border-radius: 999px;
                padding: 8px 14px;
                margin-right: 8px;
            }}

            div[role="radiogroup"] label p {{
                color: {COR_TEXTO} !important;
                font-weight: 850 !important;
                font-size: 0.95rem !important;
            }}

            .kpi-card {{
                background: {COR_CARD};
                border: 1px solid {COR_BORDA};
                border-left: 6px solid {COR_DESTAQUE};
                border-radius: 18px;
                padding: 18px 20px;
                min-height: 118px;
                box-shadow: 0 10px 28px rgba(15, 23, 42, 0.07);
                margin-bottom: 16px;
            }}

            .kpi-card.critico {{
                border-left-color: {COR_CRITICO};
                background: linear-gradient(135deg, #FFFFFF 0%, #FFF5F5 100%);
            }}

            .kpi-card.positivo {{
                border-left-color: {COR_POSITIVO};
                background: linear-gradient(135deg, #FFFFFF 0%, #F0FDF4 100%);
            }}

            .kpi-label {{
                color: {COR_TEXTO_SECUNDARIO} !important;
                font-size: 0.98rem;
                font-weight: 850;
                margin-bottom: 8px;
            }}

            .kpi-value {{
                color: {COR_TEXTO} !important;
                font-size: 1.52rem;
                font-weight: 950;
                line-height: 1.15;
                word-break: break-word;
            }}

            .kpi-value.critico {{
                color: {COR_CRITICO} !important;
            }}

            .kpi-value.positivo {{
                color: {COR_POSITIVO} !important;
            }}

            .kpi-subvalue {{
                color: {COR_TEXTO_SUAVE} !important;
                font-size: 0.92rem;
                font-weight: 750;
                margin-top: 6px;
            }}

            .regiao-card {{
                background: {COR_CARD};
                border: 1px solid {COR_BORDA};
                border-radius: 20px;
                padding: 20px;
                min-height: 260px;
                box-shadow: 0 10px 28px rgba(15, 23, 42, 0.07);
                margin-bottom: 18px;
            }}

            div[data-testid="stMetric"] {{
                background: {COR_CARD};
                border: 1px solid {COR_BORDA};
                border-radius: 18px;
                padding: 18px 20px;
                box-shadow: 0 8px 26px rgba(15, 23, 42, 0.06);
            }}

            div[data-testid="stMetricLabel"] p {{
                color: {COR_TEXTO_SECUNDARIO} !important;
                font-size: 1rem !important;
                font-weight: 850 !important;
            }}

            div[data-testid="stMetricValue"] {{
                color: {COR_TEXTO} !important;
                font-size: 1.55rem !important;
                font-weight: 950 !important;
            }}

            div[data-baseweb="select"] > div {{
                background-color: {COR_CARD} !important;
                border-color: {COR_BORDA} !important;
                color: {COR_TEXTO} !important;
            }}

            div[data-baseweb="tag"] {{
                background-color: {COR_DESTAQUE} !important;
                color: white !important;
                font-weight: 800 !important;
            }}

            div[data-baseweb="tag"] span {{
                color: white !important;
            }}

            div[data-testid="stDataFrame"] {{
                background: {COR_CARD};
                border: 1px solid {COR_BORDA};
                border-radius: 16px;
                padding: 8px;
                box-shadow: 0 8px 24px rgba(15, 23, 42, 0.04);
            }}

            hr {{
                border-color: #DDE6F3;
                margin-top: 1.8rem;
                margin-bottom: 1.8rem;
            }}
        </style>
        """,
        unsafe_allow_html=True
    )


def exibir_topo_dashboard():
    html_topo = dedent(f"""
        <div class="topo-dashboard">
            <div class="topo-dashboard__tag">Dashboard Comercial</div>
            <h1 class="topo-dashboard__titulo">{escape(NOME_EMPRESA)}</h1>
            <p class="topo-dashboard__subtitulo">{escape(SUBTITULO_DASHBOARD)}</p>
        </div>
    """).strip()

    st.markdown(html_topo, unsafe_allow_html=True)


def aplicar_layout_grafico(fig, altura=None):
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor=COR_CARD,
        plot_bgcolor=COR_CARD,
        font=dict(
            family="Arial, sans-serif",
            size=14,
            color=COR_TEXTO
        ),
        title=dict(
            font=dict(size=20, color=COR_TEXTO),
            x=0.02
        ),
        legend=dict(
            bgcolor="rgba(255,255,255,0.90)",
            bordercolor=COR_BORDA,
            borderwidth=1,
            font=dict(size=13, color=COR_TEXTO),
            title_font=dict(size=14, color=COR_TEXTO)
        ),
        margin=dict(l=45, r=45, t=78, b=45)
    )

    if altura is not None:
        fig.update_layout(height=altura)

    fig.update_xaxes(
        showgrid=True,
        gridcolor="#E5EAF2",
        zerolinecolor="#CBD5E1",
        tickfont=dict(size=13, color=COR_TEXTO),
        title_font=dict(size=14, color=COR_TEXTO)
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor="#E5EAF2",
        zerolinecolor="#CBD5E1",
        tickfont=dict(size=13, color=COR_TEXTO),
        title_font=dict(size=14, color=COR_TEXTO)
    )

    fig.update_traces(
        textfont=dict(size=13, color=COR_TEXTO),
        selector=dict(type="bar")
    )

    fig.update_traces(
        marker_line_color="#CBD5E1",
        marker_line_width=0.7,
        selector=dict(type="bar")
    )

    return fig


def exibir_grafico(fig, use_container_width=True, **kwargs):
    fig = aplicar_layout_grafico(fig)
    st.plotly_chart(fig, use_container_width=use_container_width, **kwargs)


# =========================
# FUNÇÕES AUXILIARES GERAIS
# =========================

def formatar_moeda(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def formatar_numero(valor):
    return f"{valor:,.0f}".replace(",", ".")


def formatar_percentual(valor):
    return f"{valor:.1f}%".replace(".", ",")


def dividir_seguro(numerador, denominador):
    if denominador == 0 or pd.isna(denominador):
        return 0
    return numerador / denominador


def exibir_card_kpi(titulo, valor, subtitulo=None, status="normal"):
    titulo = escape(str(titulo))
    valor = escape(str(valor))
    subtitulo_html = ""

    if subtitulo is not None:
        subtitulo_html = f'<div class="kpi-subvalue">{escape(str(subtitulo))}</div>'

    classe_card = "kpi-card"
    classe_valor = "kpi-value"

    if status == "critico":
        classe_card += " critico"
        classe_valor += " critico"
    elif status == "positivo":
        classe_card += " positivo"
        classe_valor += " positivo"

    html_card = dedent(f"""
        <div class="{classe_card}">
            <div class="kpi-label">{titulo}</div>
            <div class="{classe_valor}">{valor}</div>
            {subtitulo_html}
        </div>
    """).strip()

    st.markdown(html_card, unsafe_allow_html=True)


# =========================
# FUNÇÕES AUXILIARES — DIAGNÓSTICO PREDITIVO
# =========================

def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def normalizar_indicador(serie):
    serie = pd.to_numeric(serie, errors="coerce").fillna(0)

    minimo = serie.min()
    maximo = serie.max()

    if maximo == minimo:
        return pd.Series(0, index=serie.index)

    return (serie - minimo) / (maximo - minimo)


def preparar_base_preditiva(base_original):
    dados = base_original.copy()

    dados["receita_pred"] = pd.to_numeric(dados["receita"], errors="coerce").fillna(0)
    dados["lucro_pred"] = pd.to_numeric(dados["lucro"], errors="coerce").fillna(0)
    dados["margem_pct_pred"] = pd.to_numeric(dados["margem_lucro"], errors="coerce").fillna(0)
    dados["desconto_pct_pred"] = pd.to_numeric(dados["desconto"], errors="coerce").fillna(0)

    dados["produto_pred"] = dados["produto"].astype(str)
    dados["regiao_pred"] = dados["regiao"].astype(str)
    dados["canal_pred"] = dados["canal_venda"].astype(str)

    desconto_norm = normalizar_indicador(dados["desconto_pct_pred"])
    margem_invertida = 1 - normalizar_indicador(dados["margem_pct_pred"])
    lucro_invertido = 1 - normalizar_indicador(dados["lucro_pred"])

    dados["risco_meta_real"] = np.where(
        dados["percentual_atingimento_meta"] < LIMITE_MINIMO_META,
        1,
        0
    )

    dados["score_risco_margem"] = sigmoid(
        2.2 * desconto_norm +
        2.5 * margem_invertida -
        1.5
    )

    dados["score_risco_prejuizo"] = sigmoid(
        2.4 * lucro_invertido +
        1.5 * desconto_norm +
        1.8 * margem_invertida -
        2.0
    )

    dados["score_risco_meta"] = sigmoid(
        2.0 * desconto_norm +
        1.8 * margem_invertida +
        1.2 * dados["risco_meta_real"] -
        1.4
    )

    dados["score_geral_risco"] = (
        dados["score_risco_margem"] * 0.40 +
        dados["score_risco_prejuizo"] * 0.35 +
        dados["score_risco_meta"] * 0.25
    )

    dados["classificacao_risco"] = pd.cut(
        dados["score_geral_risco"],
        bins=[-0.01, 0.30, 0.60, 1.00],
        labels=["Baixo risco", "Médio risco", "Alto risco"]
    )

    dados["alto_risco"] = dados["score_geral_risco"] > 0.60

    return dados


# =========================
# CARREGAMENTO DOS DADOS
# =========================

CAMINHO_BASE = Path("data/processed/base_dashboard.csv")


@st.cache_data
def carregar_dados():
    df = pd.read_csv(CAMINHO_BASE)
    df["data"] = pd.to_datetime(df["data"], errors="coerce")
    return df


# =========================
# PÁGINAS DO DASHBOARD
# =========================

def pagina_visao_geral(base_filtrada):
    st.title("Visão Geral da Empresa")
    st.write("Resumo gerencial do desempenho comercial, financeiro e operacional da empresa.")

    if base_filtrada.empty:
        st.warning("Nenhum dado encontrado na base.")
        st.stop()

    receita_total = base_filtrada["receita"].sum()
    lucro_total = base_filtrada["lucro"].sum()
    margem_media = base_filtrada["margem_lucro"].mean()
    total_vendas = base_filtrada["id_venda"].nunique()
    ticket_medio = dividir_seguro(receita_total, total_vendas)
    clientes_atendidos = base_filtrada["id_cliente"].nunique()
    atingimento_medio_meta = base_filtrada["percentual_atingimento_meta"].mean()

    vendas_atrasadas = base_filtrada[
        base_filtrada["status_entrega"].str.lower().str.contains("atras", na=False)
    ]["id_venda"].nunique()

    taxa_atraso = dividir_seguro(vendas_atrasadas, total_vendas) * 100

    st.subheader("Indicadores principais")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        exibir_card_kpi("Receita líquida", formatar_moeda(receita_total), status="positivo" if receita_total > 0 else "critico")

    with col2:
        exibir_card_kpi("Lucro total", formatar_moeda(lucro_total), status="positivo" if lucro_total > 0 else "critico")

    with col3:
        exibir_card_kpi(
            "Margem média",
            formatar_percentual(margem_media),
            subtitulo=f"Alerta se abaixo de {LIMITE_MINIMO_MARGEM}%",
            status="critico" if margem_media < LIMITE_MINIMO_MARGEM else "positivo"
        )

    with col4:
        exibir_card_kpi("Total de vendas", formatar_numero(total_vendas))

    col5, col6, col7, col8 = st.columns(4)

    with col5:
        exibir_card_kpi("Ticket médio", formatar_moeda(ticket_medio))

    with col6:
        exibir_card_kpi("Clientes atendidos", formatar_numero(clientes_atendidos))

    with col7:
        exibir_card_kpi(
            "Atingimento médio da meta",
            formatar_percentual(atingimento_medio_meta),
            subtitulo=f"Alerta se abaixo de {LIMITE_MINIMO_META}%",
            status="critico" if atingimento_medio_meta < LIMITE_MINIMO_META else "positivo"
        )

    with col8:
        exibir_card_kpi(
            "Taxa de atraso",
            formatar_percentual(taxa_atraso),
            subtitulo=f"Alerta se acima de {LIMITE_MAXIMO_ATRASO}%",
            status="critico" if taxa_atraso > LIMITE_MAXIMO_ATRASO else "positivo"
        )

    st.markdown("---")
    st.subheader("Evolução mensal da receita e do lucro")

    base_mensal = (
        base_filtrada
        .groupby(["ano_mes_ordem", "mes_ano"], as_index=False)
        .agg({"receita": "sum", "lucro": "sum"})
        .sort_values("ano_mes_ordem")
    )

    base_mensal_grafico = base_mensal.melt(
        id_vars=["ano_mes_ordem", "mes_ano"],
        value_vars=["receita", "lucro"],
        var_name="Indicador",
        value_name="Valor"
    )

    base_mensal_grafico["Indicador"] = base_mensal_grafico["Indicador"].replace({
        "receita": "Receita líquida",
        "lucro": "Lucro total"
    })

    grafico_evolucao = px.line(
        base_mensal_grafico,
        x="mes_ano",
        y="Valor",
        color="Indicador",
        markers=True,
        title="Evolução mensal da receita e do lucro",
        labels={"mes_ano": "Mês/Ano", "Valor": "Valor em R$", "Indicador": "Indicador"}
    )
    exibir_grafico(grafico_evolucao, use_container_width=True)

    col_graf1, col_graf2 = st.columns(2)

    with col_graf1:
        st.subheader("Receita por canal de venda")
        base_canal = (
            base_filtrada
            .groupby("canal_venda", as_index=False)
            .agg({"receita": "sum", "lucro": "sum", "margem_lucro": "mean", "id_venda": "nunique"})
            .rename(columns={"id_venda": "total_vendas"})
            .sort_values("receita", ascending=False)
        )

        grafico_canal = px.bar(
            base_canal,
            x="canal_venda",
            y="receita",
            text="receita",
            title="Receita por canal de venda",
            labels={"canal_venda": "Canal de venda", "receita": "Receita líquida"}
        )
        grafico_canal.update_traces(texttemplate="R$ %{text:,.2f}", textposition="outside")
        exibir_grafico(grafico_canal, use_container_width=True)

    with col_graf2:
        st.subheader("Receita por região")
        base_regiao_visao = (
            base_filtrada
            .groupby("regiao", as_index=False)
            .agg({"receita": "sum", "lucro": "sum", "margem_lucro": "mean", "id_venda": "nunique"})
            .rename(columns={"id_venda": "total_vendas"})
            .sort_values("receita", ascending=True)
        )

        grafico_regiao = px.bar(
            base_regiao_visao,
            x="receita",
            y="regiao",
            orientation="h",
            text="receita",
            title="Receita por região",
            labels={"receita": "Receita líquida", "regiao": "Região"},
            hover_data={"lucro": ":,.2f", "margem_lucro": ":.1f", "total_vendas": True}
        )
        grafico_regiao.update_traces(texttemplate="R$ %{text:,.2f}", textposition="outside")
        exibir_grafico(grafico_regiao, use_container_width=True)

    st.subheader("Top 5 produtos por receita")
    base_produtos_top5 = (
        base_filtrada
        .groupby("produto", as_index=False)
        .agg({"receita": "sum", "lucro": "sum", "margem_lucro": "mean", "id_venda": "nunique"})
        .rename(columns={"id_venda": "total_vendas"})
        .sort_values("receita", ascending=False)
        .head(5)
    )

    grafico_top5_produtos = px.bar(
        base_produtos_top5,
        x="produto",
        y="receita",
        text="receita",
        title="Top 5 produtos por receita",
        labels={"produto": "Produto", "receita": "Receita líquida"},
        hover_data={"lucro": ":,.2f", "margem_lucro": ":.1f", "total_vendas": True}
    )
    grafico_top5_produtos.update_traces(texttemplate="R$ %{text:,.2f}", textposition="outside")
    exibir_grafico(grafico_top5_produtos, use_container_width=True)

    st.subheader("Realizado x Meta de Vendas")
    receita_realizada = base_filtrada["receita"].sum()
    meta_total = base_filtrada["meta_venda"].sum()
    percentual_meta = dividir_seguro(receita_realizada, meta_total) * 100

    base_meta = pd.DataFrame({"Indicador": ["Receita realizada", "Meta de vendas"], "Valor": [receita_realizada, meta_total]})

    grafico_meta = px.bar(
        base_meta,
        x="Indicador",
        y="Valor",
        text="Valor",
        title=f"Realizado x Meta de Vendas — Atingimento: {percentual_meta:.1f}%",
        labels={"Indicador": "Indicador", "Valor": "Valor em R$"}
    )
    grafico_meta.update_traces(texttemplate="R$ %{text:,.2f}", textposition="outside")
    exibir_grafico(grafico_meta, use_container_width=True)

    st.subheader("Indicador de criticidade logística")
    grafico_atraso = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=taxa_atraso,
            number={"suffix": "%", "font": {"size": 40, "color": COR_CRITICO if taxa_atraso > LIMITE_MAXIMO_ATRASO else COR_POSITIVO}},
            title={"text": "Taxa de atraso nas entregas", "font": {"size": 20, "color": COR_TEXTO}},
            gauge={
                "axis": {"range": [0, 100], "tickcolor": COR_TEXTO, "tickfont": {"color": COR_TEXTO}},
                "bar": {"color": COR_CRITICO if taxa_atraso > LIMITE_MAXIMO_ATRASO else COR_POSITIVO},
                "bgcolor": COR_CARD,
                "borderwidth": 1,
                "bordercolor": COR_BORDA,
                "steps": [
                    {"range": [0, 20], "color": "#DCFCE7"},
                    {"range": [20, 50], "color": "#FEF3C7"},
                    {"range": [50, 100], "color": "#FEE2E2"}
                ],
                "threshold": {"line": {"color": COR_DESTAQUE, "width": 4}, "thickness": 0.75, "value": taxa_atraso}
            }
        )
    )
    grafico_atraso.update_layout(height=350, margin=dict(l=20, r=20, t=60, b=20))
    exibir_grafico(grafico_atraso, use_container_width=True)


def pagina_vendas_comercial(base_filtrada):
    st.title("Vendas e Comercial")
    st.write("Análise do desempenho da equipe de vendas, considerando receita, lucro, margem, descontos, ticket médio, volume vendido e atingimento de metas.")

    if base_filtrada.empty:
        st.warning("Nenhum dado encontrado na base.")
        st.stop()

    base_vendedores = (
        base_filtrada
        .groupby("vendedor", as_index=False)
        .agg({
            "receita": "sum",
            "lucro": "sum",
            "margem_lucro": "mean",
            "desconto": "mean",
            "percentual_atingimento_meta": "mean",
            "quantidade": "sum",
            "id_venda": "nunique"
        })
        .rename(columns={"id_venda": "total_vendas"})
    )
    base_vendedores["ticket_medio"] = base_vendedores["receita"] / base_vendedores["total_vendas"]

    st.subheader("1. Desempenho financeiro por vendedor")
    st.write("Comparação entre receita e lucro para avaliar se os vendedores que mais faturam também são os que mais geram resultado financeiro.")

    top_vendedores = base_vendedores.sort_values("receita", ascending=False).head(10)
    top_vendedores_grafico = top_vendedores.melt(
        id_vars=["vendedor", "margem_lucro", "desconto", "quantidade", "total_vendas", "ticket_medio"],
        value_vars=["receita", "lucro"],
        var_name="Indicador",
        value_name="Valor"
    )
    top_vendedores_grafico["Indicador"] = top_vendedores_grafico["Indicador"].replace({"receita": "Receita", "lucro": "Lucro"})

    grafico_desempenho_vendedor = px.bar(
        top_vendedores_grafico,
        x="vendedor",
        y="Valor",
        color="Indicador",
        barmode="group",
        text="Valor",
        title="Top 10 vendedores por receita e lucro",
        labels={"vendedor": "Vendedor", "Valor": "Valor em R$", "Indicador": "Indicador"},
        hover_data={"margem_lucro": ":.2f", "desconto": ":.2f", "quantidade": True, "total_vendas": True, "ticket_medio": ":,.2f"}
    )
    grafico_desempenho_vendedor.update_traces(texttemplate="R$ %{text:,.2f}", textposition="outside")
    exibir_grafico(grafico_desempenho_vendedor, use_container_width=True)

    st.markdown("---")
    st.subheader("2. Atingimento das metas comerciais")

    base_meta_vendedor = base_vendedores.sort_values("percentual_atingimento_meta", ascending=True)
    grafico_meta_vendedor = px.bar(
        base_meta_vendedor,
        x="percentual_atingimento_meta",
        y="vendedor",
        orientation="h",
        text="percentual_atingimento_meta",
        title="Atingimento médio da meta por vendedor",
        labels={"percentual_atingimento_meta": "Atingimento médio da meta (%)", "vendedor": "Vendedor"},
        hover_data={"receita": ":,.2f", "lucro": ":,.2f", "total_vendas": True}
    )
    grafico_meta_vendedor.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    exibir_grafico(grafico_meta_vendedor, use_container_width=True)

    st.markdown("---")
    st.subheader("3. Impacto dos descontos na rentabilidade")

    grafico_desconto_margem = px.scatter(
        base_vendedores,
        x="desconto",
        y="margem_lucro",
        size="receita",
        hover_name="vendedor",
        title="Desconto médio x margem de lucro por vendedor",
        labels={"desconto": "Desconto médio (%)", "margem_lucro": "Margem de lucro média (%)", "receita": "Receita"},
        hover_data={"receita": ":,.2f", "lucro": ":,.2f", "ticket_medio": ":,.2f", "total_vendas": True}
    )
    exibir_grafico(grafico_desconto_margem, use_container_width=True)

    st.markdown("---")
    st.subheader("4. Desempenho por canal de venda")

    base_canal_comercial = (
        base_filtrada
        .groupby("canal_venda", as_index=False)
        .agg({"receita": "sum", "lucro": "sum", "margem_lucro": "mean", "id_venda": "nunique"})
        .rename(columns={"id_venda": "total_vendas"})
    )

    vendas_atrasadas_canal = (
        base_filtrada[base_filtrada["status_entrega"].str.lower().str.contains("atras", na=False)]
        .groupby("canal_venda", as_index=False)
        .agg({"id_venda": "nunique"})
        .rename(columns={"id_venda": "vendas_atrasadas"})
    )

    base_canal_comercial = base_canal_comercial.merge(vendas_atrasadas_canal, on="canal_venda", how="left")
    base_canal_comercial["vendas_atrasadas"] = base_canal_comercial["vendas_atrasadas"].fillna(0)
    base_canal_comercial["taxa_atraso"] = dividir_seguro(base_canal_comercial["vendas_atrasadas"], base_canal_comercial["total_vendas"]) * 100

    base_canal_grafico = base_canal_comercial.melt(
        id_vars=["canal_venda"],
        value_vars=["receita", "lucro"],
        var_name="Indicador",
        value_name="Valor"
    )
    base_canal_grafico["Indicador"] = base_canal_grafico["Indicador"].replace({"receita": "Receita", "lucro": "Lucro"})

    col_canal1, col_canal2 = st.columns(2)

    with col_canal1:
        grafico_canal_valor = px.bar(
            base_canal_grafico,
            x="canal_venda",
            y="Valor",
            color="Indicador",
            barmode="group",
            text="Valor",
            title="Receita e lucro por canal de venda",
            labels={"canal_venda": "Canal de venda", "Valor": "Valor em R$", "Indicador": "Indicador"}
        )
        grafico_canal_valor.update_traces(texttemplate="R$ %{text:,.2f}", textposition="outside")
        exibir_grafico(grafico_canal_valor, use_container_width=True)

    with col_canal2:
        grafico_canal_atraso = px.bar(
            base_canal_comercial,
            x="canal_venda",
            y="taxa_atraso",
            text="taxa_atraso",
            title="Taxa de atraso por canal de venda",
            labels={"canal_venda": "Canal de venda", "taxa_atraso": "Taxa de atraso (%)"},
            hover_data={"margem_lucro": ":.2f", "total_vendas": True}
        )
        grafico_canal_atraso.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        exibir_grafico(grafico_canal_atraso, use_container_width=True)

    st.markdown("---")
    st.subheader("5. Ticket médio e volume de vendas")

    grafico_ticket_volume = px.scatter(
        base_vendedores,
        x="quantidade",
        y="ticket_medio",
        size="receita",
        hover_name="vendedor",
        title="Volume vendido x ticket médio por vendedor",
        labels={"quantidade": "Quantidade vendida", "ticket_medio": "Ticket médio em R$", "receita": "Receita"},
        hover_data={"receita": ":,.2f", "lucro": ":,.2f", "margem_lucro": ":.2f", "desconto": ":.2f"}
    )
    exibir_grafico(grafico_ticket_volume, use_container_width=True)


def pagina_analise_regional(base_filtrada):
    st.title("Análise Regional")
    st.write("Análise do desempenho por região, considerando receita, lucro, margem, volume de vendas, ticket médio, desconto médio e taxa de atraso.")

    if base_filtrada.empty:
        st.warning("Nenhum dado encontrado na base.")
        st.stop()

    base_regiao = (
        base_filtrada
        .groupby("regiao", as_index=False)
        .agg({"receita": "sum", "lucro": "sum", "margem_lucro": "mean", "desconto": "mean", "quantidade": "sum", "id_venda": "nunique"})
        .rename(columns={"id_venda": "total_vendas"})
    )

    base_regiao["ticket_medio"] = base_regiao["receita"] / base_regiao["total_vendas"]
    receita_total_regional = base_regiao["receita"].sum()
    base_regiao["participacao_receita"] = dividir_seguro(base_regiao["receita"], receita_total_regional) * 100

    vendas_atrasadas_regiao = (
        base_filtrada[base_filtrada["status_entrega"].str.lower().str.contains("atras", na=False)]
        .groupby("regiao", as_index=False)
        .agg({"id_venda": "nunique"})
        .rename(columns={"id_venda": "vendas_atrasadas"})
    )

    base_regiao = base_regiao.merge(vendas_atrasadas_regiao, on="regiao", how="left")
    base_regiao["vendas_atrasadas"] = base_regiao["vendas_atrasadas"].fillna(0)
    base_regiao["taxa_atraso"] = dividir_seguro(base_regiao["vendas_atrasadas"], base_regiao["total_vendas"]) * 100
    base_regiao = base_regiao.sort_values("receita", ascending=False)

    st.subheader("1. Receita e lucro por região")
    base_regiao_valores = base_regiao.melt(
        id_vars=["regiao", "margem_lucro", "taxa_atraso", "desconto", "ticket_medio", "total_vendas"],
        value_vars=["receita", "lucro"],
        var_name="Indicador",
        value_name="Valor"
    )
    base_regiao_valores["Indicador"] = base_regiao_valores["Indicador"].replace({"receita": "Receita", "lucro": "Lucro"})

    grafico_receita_lucro_regiao = px.bar(
        base_regiao_valores,
        x="regiao",
        y="Valor",
        color="Indicador",
        barmode="group",
        text="Valor",
        title="Receita e lucro por região",
        labels={"regiao": "Região", "Valor": "Valor em R$", "Indicador": "Indicador"},
        hover_data={"margem_lucro": ":.2f", "taxa_atraso": ":.2f", "desconto": ":.2f", "ticket_medio": ":,.2f", "total_vendas": True}
    )
    grafico_receita_lucro_regiao.update_traces(texttemplate="R$ %{text:,.2f}", textposition="outside")
    exibir_grafico(grafico_receita_lucro_regiao, use_container_width=True)

    st.markdown("---")
    st.subheader("2. Matriz regional: margem x taxa de atraso")

    grafico_margem_atraso = px.scatter(
        base_regiao,
        x="taxa_atraso",
        y="margem_lucro",
        size="receita",
        hover_name="regiao",
        title="Margem de lucro x taxa de atraso por região",
        labels={"taxa_atraso": "Taxa de atraso (%)", "margem_lucro": "Margem de lucro média (%)", "receita": "Receita"},
        hover_data={"receita": ":,.2f", "lucro": ":,.2f", "desconto": ":.2f", "ticket_medio": ":,.2f", "total_vendas": True}
    )
    exibir_grafico(grafico_margem_atraso, use_container_width=True)

    st.markdown("---")
    st.subheader("3. Evolução trimestral da receita por região")

    base_trimestre = base_filtrada.copy()
    base_trimestre["trimestre_label"] = base_trimestre["ano"].astype(str) + " - T" + base_trimestre["trimestre"].astype(str)

    base_trimestre_regiao = (
        base_trimestre
        .groupby(["ano", "trimestre", "trimestre_label", "regiao"], as_index=False)
        .agg({"receita": "sum"})
        .sort_values(["ano", "trimestre"])
    )

    grafico_trimestre_regiao = px.line(
        base_trimestre_regiao,
        x="trimestre_label",
        y="receita",
        color="regiao",
        markers=True,
        title="Evolução trimestral da receita por região",
        labels={"trimestre_label": "Trimestre", "receita": "Receita em R$", "regiao": "Região"}
    )
    exibir_grafico(grafico_trimestre_regiao, use_container_width=True)

    st.markdown("---")
    st.subheader("4. Taxa de atraso por região")

    base_atraso_regiao = base_regiao.sort_values("taxa_atraso", ascending=True)
    grafico_atraso_regiao = px.bar(
        base_atraso_regiao,
        x="taxa_atraso",
        y="regiao",
        orientation="h",
        text="taxa_atraso",
        title="Taxa de atraso por região",
        labels={"taxa_atraso": "Taxa de atraso (%)", "regiao": "Região"},
        hover_data={"receita": ":,.2f", "lucro": ":,.2f", "margem_lucro": ":.2f", "total_vendas": True}
    )
    grafico_atraso_regiao.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    exibir_grafico(grafico_atraso_regiao, use_container_width=True)

    st.markdown("---")
    st.subheader("5. Receita por marca e região")

    base_marca_regiao = (
        base_filtrada
        .groupby(["regiao", "marca"], as_index=False)
        .agg({"receita": "sum"})
        .sort_values("receita", ascending=False)
    )

    grafico_marca_regiao = px.bar(
        base_marca_regiao,
        x="regiao",
        y="receita",
        color="marca",
        title="Receita por marca dentro de cada região",
        labels={"regiao": "Região", "receita": "Receita em R$", "marca": "Marca"}
    )
    exibir_grafico(grafico_marca_regiao, use_container_width=True)


def pagina_analise_produtos(base_filtrada):
    st.title("Análise de Produtos")
    st.write("Análise do portfólio de produtos considerando receita, lucro, margem, giro, linha de produto, canal de venda, prejuízos em vendas negativas e logística.")

    if base_filtrada.empty:
        st.warning("Nenhum dado encontrado na base.")
        st.stop()

    st.markdown("### Filtros específicos de produtos")
    col_filtro1, col_filtro2, col_filtro3 = st.columns(3)

    produtos_disponiveis = sorted(base_filtrada["produto"].dropna().unique())
    marcas_disponiveis = sorted(base_filtrada["marca"].dropna().unique())
    linhas_disponiveis = sorted(base_filtrada["linha_produto"].dropna().unique())

    with col_filtro1:
        filtro_produto_pagina = st.multiselect("Produto", options=produtos_disponiveis, default=produtos_disponiveis)

    with col_filtro2:
        filtro_marca_pagina = st.multiselect("Marca", options=marcas_disponiveis, default=marcas_disponiveis)

    with col_filtro3:
        filtro_linha_pagina = st.multiselect("Linha do produto", options=linhas_disponiveis, default=linhas_disponiveis)

    base_produtos_filtrada = base_filtrada[
        (base_filtrada["produto"].isin(filtro_produto_pagina)) &
        (base_filtrada["marca"].isin(filtro_marca_pagina)) &
        (base_filtrada["linha_produto"].isin(filtro_linha_pagina))
    ]

    if base_produtos_filtrada.empty:
        st.warning("Nenhum dado encontrado para os filtros de produtos selecionados.")
        st.stop()

    base_produtos = (
        base_produtos_filtrada
        .groupby("produto", as_index=False)
        .agg({
            "receita": "sum",
            "lucro": "sum",
            "quantidade": "sum",
            "id_venda": "nunique",
            "desconto": "mean",
            "valor_desconto": "sum",
            "prazo_entrega_dias": "mean"
        })
        .rename(columns={"id_venda": "numero_vendas"})
    )

    base_produto_info = (
        base_produtos_filtrada
        .groupby("produto", as_index=False)
        .agg({
            "categoria": lambda x: x.mode().iloc[0] if not x.mode().empty else x.iloc[0],
            "linha_produto": lambda x: x.mode().iloc[0] if not x.mode().empty else x.iloc[0]
        })
    )

    base_produtos = base_produtos.merge(base_produto_info, on="produto", how="left")
    base_produtos["margem_lucro_produto"] = base_produtos.apply(lambda linha: dividir_seguro(linha["lucro"], linha["receita"]) * 100, axis=1)
    base_produtos["ticket_medio"] = base_produtos.apply(lambda linha: dividir_seguro(linha["receita"], linha["numero_vendas"]), axis=1)
    base_produtos["preco_medio_vendido"] = base_produtos.apply(lambda linha: dividir_seguro(linha["receita"], linha["quantidade"]), axis=1)

    receita_total_produtos = base_produtos["receita"].sum()
    lucro_total_produtos = base_produtos["lucro"].sum()
    unidades_vendidas = base_produtos["quantidade"].sum()
    margem_geral_produtos = dividir_seguro(lucro_total_produtos, receita_total_produtos) * 100

    base_produtos["participacao_receita"] = dividir_seguro(base_produtos["receita"], receita_total_produtos) * 100
    base_produtos["participacao_lucro"] = dividir_seguro(base_produtos["lucro"], lucro_total_produtos) * 100 if lucro_total_produtos > 0 else 0

    vendas_prejuizo = (
        base_produtos_filtrada[base_produtos_filtrada["lucro"] < 0]
        .groupby("produto", as_index=False)
        .agg({"id_venda": "nunique", "lucro": "sum"})
        .rename(columns={"id_venda": "vendas_prejuizo", "lucro": "prejuizo_acumulado"})
    )

    base_produtos = base_produtos.merge(vendas_prejuizo, on="produto", how="left")
    base_produtos["vendas_prejuizo"] = base_produtos["vendas_prejuizo"].fillna(0)
    base_produtos["prejuizo_acumulado"] = base_produtos["prejuizo_acumulado"].fillna(0)
    base_produtos["valor_prejuizo_acumulado"] = base_produtos["prejuizo_acumulado"].abs()
    base_produtos["taxa_vendas_prejuizo"] = dividir_seguro(base_produtos["vendas_prejuizo"], base_produtos["numero_vendas"]) * 100

    vendas_atrasadas_produto = (
        base_produtos_filtrada[base_produtos_filtrada["status_entrega"].str.lower().str.contains("atras", na=False)]
        .groupby("produto", as_index=False)
        .agg({"id_venda": "nunique"})
        .rename(columns={"id_venda": "pedidos_atrasados"})
    )

    base_produtos = base_produtos.merge(vendas_atrasadas_produto, on="produto", how="left")
    base_produtos["pedidos_atrasados"] = base_produtos["pedidos_atrasados"].fillna(0)
    base_produtos["taxa_atraso"] = dividir_seguro(base_produtos["pedidos_atrasados"], base_produtos["numero_vendas"]) * 100

    base_linha = (
        base_produtos_filtrada
        .groupby("linha_produto", as_index=False)
        .agg({"receita": "sum", "lucro": "sum", "id_venda": "nunique"})
        .rename(columns={"id_venda": "numero_vendas"})
    )
    base_linha["margem_lucro"] = base_linha.apply(lambda linha: dividir_seguro(linha["lucro"], linha["receita"]) * 100, axis=1)
    base_linha["participacao_lucro"] = dividir_seguro(base_linha["lucro"], base_linha["lucro"].sum()) * 100 if base_linha["lucro"].sum() > 0 else 0

    produto_lider_receita = base_produtos.sort_values("receita", ascending=False).iloc[0]
    produto_mais_rentavel = base_produtos.sort_values("margem_lucro_produto", ascending=False).iloc[0]
    produto_maior_prejuizo = base_produtos.sort_values("valor_prejuizo_acumulado", ascending=False).iloc[0]
    produto_maior_atraso = base_produtos.sort_values("taxa_atraso", ascending=False).iloc[0]

    st.subheader("Indicadores principais do portfólio")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        exibir_card_kpi("Receita total", formatar_moeda(receita_total_produtos), status="positivo" if receita_total_produtos > 0 else "critico")
    with col2:
        exibir_card_kpi("Lucro total", formatar_moeda(lucro_total_produtos), status="positivo" if lucro_total_produtos > 0 else "critico")
    with col3:
        exibir_card_kpi("Margem geral", formatar_percentual(margem_geral_produtos), status="critico" if margem_geral_produtos < LIMITE_MINIMO_MARGEM else "positivo")
    with col4:
        exibir_card_kpi("Unidades vendidas", formatar_numero(unidades_vendidas))

    col5, col6, col7, col8 = st.columns(4)
    with col5:
        exibir_card_kpi("Produto líder em receita", produto_lider_receita["produto"], formatar_moeda(produto_lider_receita["receita"]))
    with col6:
        exibir_card_kpi("Produto mais rentável", produto_mais_rentavel["produto"], formatar_percentual(produto_mais_rentavel["margem_lucro_produto"]), status="critico" if produto_mais_rentavel["margem_lucro_produto"] < LIMITE_MINIMO_MARGEM else "positivo")
    with col7:
        exibir_card_kpi("Produto com maior prejuízo", produto_maior_prejuizo["produto"], formatar_moeda(produto_maior_prejuizo["valor_prejuizo_acumulado"]), status="critico" if produto_maior_prejuizo["valor_prejuizo_acumulado"] > 0 else "normal")
    with col8:
        exibir_card_kpi("Produto com maior atraso", produto_maior_atraso["produto"], formatar_percentual(produto_maior_atraso["taxa_atraso"]), status="critico" if produto_maior_atraso["taxa_atraso"] > LIMITE_MAXIMO_ATRASO else "positivo")

    st.markdown("---")
    st.subheader("1. Desempenho financeiro por produto")

    base_financeiro = base_produtos.sort_values("receita", ascending=False)
    base_financeiro_grafico = base_financeiro.melt(
        id_vars=["produto", "margem_lucro_produto", "participacao_receita", "participacao_lucro"],
        value_vars=["receita", "lucro"],
        var_name="Indicador",
        value_name="Valor"
    )
    base_financeiro_grafico["Indicador"] = base_financeiro_grafico["Indicador"].replace({"receita": "Receita", "lucro": "Lucro"})

    grafico_financeiro_produto = px.bar(
        base_financeiro_grafico,
        x="produto",
        y="Valor",
        color="Indicador",
        barmode="group",
        text="Valor",
        title="Receita x lucro por produto",
        labels={"produto": "Produto", "Valor": "Valor em R$", "Indicador": "Indicador"},
        hover_data={"margem_lucro_produto": ":.2f", "participacao_receita": ":.2f", "participacao_lucro": ":.2f"}
    )
    grafico_financeiro_produto.update_traces(texttemplate="R$ %{text:,.2f}", textposition="outside")
    exibir_grafico(grafico_financeiro_produto, use_container_width=True)

    st.markdown("---")
    st.subheader("2. Volume e giro de produtos")

    base_volume = base_produtos.sort_values("quantidade", ascending=False)
    grafico_volume_ticket = go.Figure()
    grafico_volume_ticket.add_trace(go.Bar(x=base_volume["produto"], y=base_volume["quantidade"], name="Unidades vendidas", text=base_volume["quantidade"], textposition="outside"))
    grafico_volume_ticket.add_trace(go.Scatter(x=base_volume["produto"], y=base_volume["ticket_medio"], name="Ticket médio", mode="lines+markers", yaxis="y2"))
    grafico_volume_ticket.update_layout(
        title="Unidades vendidas x ticket médio por produto",
        xaxis_title="Produto",
        yaxis=dict(title="Unidades vendidas"),
        yaxis2=dict(title="Ticket médio em R$", overlaying="y", side="right"),
        legend_title_text="Indicador"
    )
    exibir_grafico(grafico_volume_ticket, use_container_width=True)

    st.markdown("---")
    st.subheader("3. Participação dos produtos no lucro")

    base_participacao_lucro = base_produtos.sort_values("participacao_lucro", ascending=True)
    grafico_participacao_lucro = px.bar(
        base_participacao_lucro,
        x="participacao_lucro",
        y="produto",
        orientation="h",
        text="participacao_lucro",
        title="Participação dos produtos no lucro total",
        labels={"participacao_lucro": "Participação no lucro (%)", "produto": "Produto"},
        hover_data={"receita": ":,.2f", "lucro": ":,.2f", "margem_lucro_produto": ":.2f"}
    )
    grafico_participacao_lucro.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    exibir_grafico(grafico_participacao_lucro, use_container_width=True)

    st.markdown("---")
    st.subheader("4. Produtos Premium, Padrão e Econômico")

    base_linha_ordenada = base_linha.sort_values("receita", ascending=False)
    grafico_linha = go.Figure()
    grafico_linha.add_trace(go.Bar(x=base_linha_ordenada["linha_produto"], y=base_linha_ordenada["receita"], name="Receita", text=base_linha_ordenada["receita"], texttemplate="R$ %{text:,.2f}", textposition="outside"))
    grafico_linha.add_trace(go.Bar(x=base_linha_ordenada["linha_produto"], y=base_linha_ordenada["lucro"], name="Lucro", text=base_linha_ordenada["lucro"], texttemplate="R$ %{text:,.2f}", textposition="outside"))
    grafico_linha.add_trace(go.Scatter(x=base_linha_ordenada["linha_produto"], y=base_linha_ordenada["margem_lucro"], name="Margem", mode="lines+markers", yaxis="y2"))
    grafico_linha.update_layout(
        title="Receita, lucro e margem por linha de produto",
        barmode="group",
        xaxis_title="Linha do produto",
        yaxis=dict(title="Valor em R$"),
        yaxis2=dict(title="Margem (%)", overlaying="y", side="right"),
        legend_title_text="Indicador"
    )
    exibir_grafico(grafico_linha, use_container_width=True)

    st.markdown("---")
    st.subheader("5. Produto x canal de venda")

    base_produto_canal = base_produtos_filtrada.groupby(["produto", "canal_venda"], as_index=False).agg({"receita": "sum"})
    total_produto_canal = base_produto_canal.groupby("produto", as_index=False).agg({"receita": "sum"}).rename(columns={"receita": "receita_total_produto"})
    base_produto_canal = base_produto_canal.merge(total_produto_canal, on="produto", how="left")
    base_produto_canal["participacao_canal"] = dividir_seguro(base_produto_canal["receita"], base_produto_canal["receita_total_produto"]) * 100

    grafico_produto_canal = px.bar(
        base_produto_canal,
        x="produto",
        y="participacao_canal",
        color="canal_venda",
        title="Participação da receita por produto e canal de venda",
        labels={"produto": "Produto", "participacao_canal": "% da receita do produto", "canal_venda": "Canal de venda"},
        hover_data={"receita": ":,.2f"}
    )
    grafico_produto_canal.update_layout(barmode="stack")
    exibir_grafico(grafico_produto_canal, use_container_width=True)

    st.markdown("---")
    st.subheader("6. Premium por canal de venda")

    base_premium = base_produtos_filtrada[base_produtos_filtrada["linha_produto"].str.lower().str.contains("premium", na=False)]

    if base_premium.empty:
        st.warning("Não há dados da linha Premium para os filtros selecionados.")
    else:
        base_premium_canal = (
            base_premium
            .groupby("canal_venda", as_index=False)
            .agg({"receita": "sum", "lucro": "sum", "id_venda": "nunique"})
            .rename(columns={"id_venda": "numero_vendas"})
        )
        base_premium_canal["margem"] = dividir_seguro(base_premium_canal["lucro"], base_premium_canal["receita"]) * 100

        premium_atrasado = (
            base_premium[base_premium["status_entrega"].str.lower().str.contains("atras", na=False)]
            .groupby("canal_venda", as_index=False)
            .agg({"id_venda": "nunique"})
            .rename(columns={"id_venda": "pedidos_atrasados"})
        )
        base_premium_canal = base_premium_canal.merge(premium_atrasado, on="canal_venda", how="left")
        base_premium_canal["pedidos_atrasados"] = base_premium_canal["pedidos_atrasados"].fillna(0)
        base_premium_canal["taxa_atraso"] = dividir_seguro(base_premium_canal["pedidos_atrasados"], base_premium_canal["numero_vendas"]) * 100

        base_premium_canal_grafico = base_premium_canal.melt(
            id_vars=["canal_venda", "margem", "taxa_atraso"],
            value_vars=["receita", "lucro"],
            var_name="Indicador",
            value_name="Valor"
        )
        base_premium_canal_grafico["Indicador"] = base_premium_canal_grafico["Indicador"].replace({"receita": "Receita Premium", "lucro": "Lucro Premium"})

        grafico_premium_canal = px.bar(
            base_premium_canal_grafico,
            x="canal_venda",
            y="Valor",
            color="Indicador",
            barmode="group",
            text="Valor",
            title="Receita e lucro Premium por canal",
            labels={"canal_venda": "Canal de venda", "Valor": "Valor em R$", "Indicador": "Indicador"},
            hover_data={"margem": ":.2f", "taxa_atraso": ":.2f"}
        )
        grafico_premium_canal.update_traces(texttemplate="R$ %{text:,.2f}", textposition="outside")
        exibir_grafico(grafico_premium_canal, use_container_width=True)

    st.markdown("---")
    st.subheader("7. Produtos Premium mais relevantes")

    if base_premium.empty:
        st.warning("Não há dados da linha Premium para os filtros selecionados.")
    else:
        base_produtos_premium = (
            base_premium
            .groupby("produto", as_index=False)
            .agg({"receita": "sum", "lucro": "sum", "id_venda": "nunique"})
            .rename(columns={"id_venda": "numero_vendas"})
        )
        base_produtos_premium["margem"] = dividir_seguro(base_produtos_premium["lucro"], base_produtos_premium["receita"]) * 100
        base_produtos_premium = base_produtos_premium.sort_values("lucro", ascending=True)

        grafico_produtos_premium = px.bar(
            base_produtos_premium,
            x="lucro",
            y="produto",
            orientation="h",
            text="lucro",
            title="Lucro dos produtos Premium",
            labels={"lucro": "Lucro em R$", "produto": "Produto", "receita": "Receita", "margem": "Margem (%)", "numero_vendas": "Número de vendas"},
            hover_data={"receita": ":,.2f", "margem": ":.2f", "numero_vendas": True}
        )
        grafico_produtos_premium.update_traces(texttemplate="R$ %{text:,.2f}", textposition="outside")
        exibir_grafico(grafico_produtos_premium, use_container_width=True)

    st.markdown("---")
    st.subheader("8. Produtos com maior prejuízo em vendas negativas")

    base_prejuizo = base_produtos.sort_values("valor_prejuizo_acumulado", ascending=True)
    grafico_prejuizo = px.bar(
        base_prejuizo,
        x="valor_prejuizo_acumulado",
        y="produto",
        orientation="h",
        text="valor_prejuizo_acumulado",
        title="Prejuízo acumulado em vendas negativas por produto",
        labels={"valor_prejuizo_acumulado": "Prejuízo acumulado em R$", "produto": "Produto"},
        hover_data={"vendas_prejuizo": True, "taxa_vendas_prejuizo": ":.2f", "receita": ":,.2f", "lucro": ":,.2f"}
    )
    grafico_prejuizo.update_traces(texttemplate="R$ %{text:,.2f}", textposition="outside")
    exibir_grafico(grafico_prejuizo, use_container_width=True)

    st.markdown("---")
    st.subheader("9. Logística por produto")

    base_logistica = base_produtos.sort_values("taxa_atraso", ascending=True)
    grafico_atraso_produto = px.bar(
        base_logistica,
        x="taxa_atraso",
        y="produto",
        orientation="h",
        text="taxa_atraso",
        title="Taxa de atraso por produto",
        labels={"taxa_atraso": "Taxa de atraso (%)", "produto": "Produto"},
        hover_data={"prazo_entrega_dias": ":.2f", "pedidos_atrasados": True, "numero_vendas": True, "receita": ":,.2f", "lucro": ":,.2f"}
    )
    grafico_atraso_produto.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    exibir_grafico(grafico_atraso_produto, use_container_width=True)


def pagina_diagnostico_preditivo(base_filtrada):
    st.title("Diagnóstico Preditivo Comercial")
    st.write(
        "Identificação de vendas, produtos e regiões com maior risco de baixa margem, "
        "prejuízo e não atingimento de meta."
    )

    if base_filtrada.empty:
        st.warning("Nenhum dado encontrado na base.")
        st.stop()

    base_preditiva = preparar_base_preditiva(base_filtrada)

    st.markdown("### Filtros da análise preditiva")
    col_filtro1, col_filtro2, col_filtro3 = st.columns(3)

    produtos_disponiveis = sorted(base_preditiva["produto_pred"].dropna().unique())
    regioes_disponiveis = sorted(base_preditiva["regiao_pred"].dropna().unique())
    canais_disponiveis = sorted(base_preditiva["canal_pred"].dropna().unique())

    with col_filtro1:
        filtro_produtos_pred = st.multiselect("Produto", options=produtos_disponiveis, default=produtos_disponiveis)

    with col_filtro2:
        filtro_regioes_pred = st.multiselect("Região", options=regioes_disponiveis, default=regioes_disponiveis)

    with col_filtro3:
        filtro_canais_pred = st.multiselect("Canal de venda", options=canais_disponiveis, default=canais_disponiveis)

    base_preditiva_filtrada = base_preditiva[
        (base_preditiva["produto_pred"].isin(filtro_produtos_pred)) &
        (base_preditiva["regiao_pred"].isin(filtro_regioes_pred)) &
        (base_preditiva["canal_pred"].isin(filtro_canais_pred))
    ]

    if base_preditiva_filtrada.empty:
        st.warning("Nenhum dado encontrado para os filtros selecionados.")
        st.stop()

    st.markdown("---")

    score_geral = base_preditiva_filtrada["score_geral_risco"].mean()
    prob_margem_baixa = base_preditiva_filtrada["score_risco_margem"].mean()
    prob_prejuizo = base_preditiva_filtrada["score_risco_prejuizo"].mean()

    receita_em_risco = base_preditiva_filtrada.loc[base_preditiva_filtrada["alto_risco"], "receita_pred"].sum()
    perc_vendas_alto_risco = base_preditiva_filtrada["alto_risco"].mean() * 100
    desconto_medio_risco = base_preditiva_filtrada.loc[base_preditiva_filtrada["alto_risco"], "desconto_pct_pred"].mean()

    if pd.isna(desconto_medio_risco):
        desconto_medio_risco = 0

    st.subheader("KPIs de atenção preditiva")
    col1, col2, col3 = st.columns(3)

    with col1:
        exibir_card_kpi("Score geral de risco", formatar_percentual(score_geral * 100), "Combina risco de margem, prejuízo e meta.", status="critico" if score_geral > 0.60 else "positivo")
    with col2:
        exibir_card_kpi("Receita em risco", formatar_moeda(receita_em_risco), "Receita concentrada em vendas de alto risco.", status="critico" if receita_em_risco > 0 else "positivo")
    with col3:
        exibir_card_kpi("% vendas em alto risco", formatar_percentual(perc_vendas_alto_risco), "Participação das vendas classificadas como alto risco.", status="critico" if perc_vendas_alto_risco > 30 else "positivo")

    col4, col5, col6 = st.columns(3)

    with col4:
        exibir_card_kpi("Prob. margem baixa", formatar_percentual(prob_margem_baixa * 100), "Chance média de margem comercial pressionada.", status="critico" if prob_margem_baixa > 0.60 else "positivo")
    with col5:
        exibir_card_kpi("Prob. prejuízo", formatar_percentual(prob_prejuizo * 100), "Chance média de resultado negativo.", status="critico" if prob_prejuizo > 0.60 else "positivo")
    with col6:
        exibir_card_kpi("Desconto médio em risco", formatar_percentual(desconto_medio_risco), "Desconto médio das vendas classificadas como alto risco.", status="critico" if desconto_medio_risco > 15 else "positivo")

    st.markdown("---")
    st.subheader("1. Risco de rentabilidade")
    st.write("Relação entre desconto e margem de lucro para identificar vendas com maior risco de perda de rentabilidade.")

    col_graf1, col_graf2 = st.columns([1.3, 1])

    with col_graf1:
        desconto_margem_produto = (
            base_preditiva_filtrada
            .groupby("produto_pred", as_index=False)
            .agg({
                "desconto_pct_pred": "mean",
                "margem_pct_pred": "mean",
                "receita_pred": "sum",
                "lucro_pred": "sum",
                "score_geral_risco": "mean",
                "score_risco_margem": "mean",
                "score_risco_prejuizo": "mean",
                "score_risco_meta": "mean",
                "id_venda": "nunique"
            })
            .rename(columns={"id_venda": "total_vendas"})
        )

        desconto_margem_produto["classificacao_risco"] = pd.cut(
            desconto_margem_produto["score_geral_risco"],
            bins=[-0.01, 0.30, 0.60, 1.00],
            labels=["Baixo risco", "Médio risco", "Alto risco"]
        )

        grafico_desconto_margem_pred = px.scatter(
            desconto_margem_produto,
            x="desconto_pct_pred",
            y="margem_pct_pred",
            size="receita_pred",
            color="classificacao_risco",
            hover_name="produto_pred",
            title="Desconto médio x margem de lucro por produto",
            labels={
                "desconto_pct_pred": "Desconto médio (%)",
                "margem_pct_pred": "Margem de lucro média (%)",
                "receita_pred": "Receita total",
                "lucro_pred": "Lucro total",
                "classificacao_risco": "Classificação de risco",
                "produto_pred": "Produto",
                "score_geral_risco": "Score geral",
                "score_risco_margem": "Risco de margem",
                "score_risco_prejuizo": "Risco de prejuízo",
                "score_risco_meta": "Risco de meta",
                "total_vendas": "Total de vendas"
            },
            hover_data={
                "receita_pred": ":,.2f",
                "lucro_pred": ":,.2f",
                "total_vendas": True,
                "score_geral_risco": ":.2%",
                "score_risco_margem": ":.2%",
                "score_risco_prejuizo": ":.2%",
                "score_risco_meta": ":.2%"
            }
        )

        grafico_desconto_margem_pred.update_layout(
            xaxis_title="Desconto médio (%)",
            yaxis_title="Margem de lucro média (%)",
            legend_title_text="Classificação"
        )

        exibir_grafico(grafico_desconto_margem_pred, use_container_width=True)

    with col_graf2:
        produtos_risco_margem = (
            base_preditiva_filtrada
            .groupby("produto_pred", as_index=False)
            .agg({"score_risco_margem": "mean", "receita_pred": "sum", "margem_pct_pred": "mean"})
            .sort_values("score_risco_margem", ascending=True)
            .tail(8)
        )

        grafico_produtos_margem = px.bar(
            produtos_risco_margem,
            x="score_risco_margem",
            y="produto_pred",
            orientation="h",
            text="score_risco_margem",
            title="Produtos com maior risco de margem baixa",
            labels={"score_risco_margem": "Risco de margem baixa", "produto_pred": "Produto"},
            hover_data={"receita_pred": ":,.2f", "margem_pct_pred": ":.2f"}
        )
        grafico_produtos_margem.update_traces(texttemplate="%{text:.1%}", textposition="outside")
        exibir_grafico(grafico_produtos_margem, use_container_width=True)

    st.markdown("---")
    st.subheader("2. Risco de prejuízo")
    st.write("Identificação de produtos e regiões com maior probabilidade de gerar resultado negativo.")

    base_preditiva_filtrada = base_preditiva_filtrada.copy()
    base_preditiva_filtrada["receita_alto_risco"] = np.where(
        base_preditiva_filtrada["alto_risco"],
        base_preditiva_filtrada["receita_pred"],
        0
    )

    col_graf3, col_graf4 = st.columns(2)

    with col_graf3:
        risco_prejuizo_regiao = (
            base_preditiva_filtrada
            .groupby("regiao_pred", as_index=False)
            .agg({"score_risco_prejuizo": "mean", "receita_alto_risco": "sum", "lucro_pred": "sum"})
            .sort_values("score_risco_prejuizo", ascending=False)
        )

        grafico_risco_regiao = px.bar(
            risco_prejuizo_regiao,
            x="regiao_pred",
            y="score_risco_prejuizo",
            text="score_risco_prejuizo",
            title="Risco de prejuízo por região",
            labels={"regiao_pred": "Região", "score_risco_prejuizo": "Probabilidade de prejuízo"},
            hover_data={"receita_alto_risco": ":,.2f", "lucro_pred": ":,.2f"}
        )
        grafico_risco_regiao.update_traces(texttemplate="%{text:.1%}", textposition="outside")
        exibir_grafico(grafico_risco_regiao, use_container_width=True)

    with col_graf4:
        risco_prejuizo_produto = (
            base_preditiva_filtrada
            .groupby("produto_pred", as_index=False)
            .agg({"score_risco_prejuizo": "mean", "receita_pred": "sum", "lucro_pred": "sum"})
            .sort_values("score_risco_prejuizo", ascending=True)
            .tail(8)
        )

        grafico_risco_produto = px.bar(
            risco_prejuizo_produto,
            x="score_risco_prejuizo",
            y="produto_pred",
            orientation="h",
            text="score_risco_prejuizo",
            title="Produtos com maior risco de prejuízo",
            labels={"score_risco_prejuizo": "Probabilidade de prejuízo", "produto_pred": "Produto"},
            hover_data={"receita_pred": ":,.2f", "lucro_pred": ":,.2f"}
        )
        grafico_risco_produto.update_traces(texttemplate="%{text:.1%}", textposition="outside")
        exibir_grafico(grafico_risco_produto, use_container_width=True)

    st.markdown("---")
    st.subheader("3. Risco de não atingir meta")
    st.write("Funil de exposição comercial com foco nas vendas que apresentam maior risco de não entregar o resultado esperado.")

    total_vendas = len(base_preditiva_filtrada)
    vendas_algum_risco = len(base_preditiva_filtrada[base_preditiva_filtrada["score_geral_risco"] > 0.30])
    vendas_alto_risco = len(base_preditiva_filtrada[base_preditiva_filtrada["score_geral_risco"] > 0.60])

    col_funil, col_meta = st.columns(2)

    with col_funil:
        grafico_funil = go.Figure(
            go.Funnel(
                y=["Total de vendas", "Vendas com algum risco", "Vendas com alto risco"],
                x=[total_vendas, vendas_algum_risco, vendas_alto_risco],
                textinfo="value+percent initial"
            )
        )
        grafico_funil.update_layout(title="Funil de risco comercial", height=420)
        exibir_grafico(grafico_funil, use_container_width=True)

    with col_meta:
        risco_meta_produto = (
            base_preditiva_filtrada
            .groupby("produto_pred", as_index=False)
            .agg({"score_risco_meta": "mean", "receita_pred": "sum", "desconto_pct_pred": "mean"})
            .sort_values("score_risco_meta", ascending=True)
            .tail(8)
        )

        grafico_meta_produto = px.bar(
            risco_meta_produto,
            x="score_risco_meta",
            y="produto_pred",
            orientation="h",
            text="score_risco_meta",
            title="Produtos com maior risco de não bater meta",
            labels={"score_risco_meta": "Risco de não atingir meta", "produto_pred": "Produto"},
            hover_data={"receita_pred": ":,.2f", "desconto_pct_pred": ":.2f"}
        )
        grafico_meta_produto.update_traces(texttemplate="%{text:.1%}", textposition="outside")
        exibir_grafico(grafico_meta_produto, use_container_width=True)

    st.markdown("---")
    st.subheader("4. Mapa de atenção comercial por região")
    st.write("Comparação dos principais riscos preditivos por região.")

    st.markdown(
        f"""
        <div class="regiao-card" style="min-height: auto; margin-top: 8px; margin-bottom: 22px;">
            <h4 style="margin-top: 0; color: {COR_TEXTO};">Como interpretar os riscos do heatmap</h4>
            <p><strong>Risco de Margem:</strong> indica a probabilidade de uma venda, produto ou região apresentar margem baixa. A metodologia considera principalmente desconto elevado e margem de lucro pressionada, normalizados em uma escala comum e convertidos em score pela função logística.</p>
            <p><strong>Risco de Prejuízo:</strong> indica a probabilidade de resultado financeiro negativo. A metodologia combina lucro baixo ou negativo, desconto elevado e margem pressionada, gerando uma probabilidade estimada de exposição ao prejuízo.</p>
            <p><strong>Risco de Meta:</strong> indica a chance de não atingir o desempenho comercial esperado. A metodologia considera desconto, margem e o percentual de atingimento da meta, com alerta quando o atingimento fica abaixo de {LIMITE_MINIMO_META}%.</p>
            <p><strong>Score Geral:</strong> consolida os três riscos em um único indicador de atenção comercial, usando os pesos: 40% risco de margem, 35% risco de prejuízo e 25% risco de meta.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    mapa_risco = (
        base_preditiva_filtrada
        .groupby("regiao_pred", as_index=False)
        .agg({
            "score_risco_margem": "mean",
            "score_risco_prejuizo": "mean",
            "score_risco_meta": "mean",
            "score_geral_risco": "mean"
        })
        .rename(columns={
            "score_risco_margem": "Risco de Margem",
            "score_risco_prejuizo": "Risco de Prejuízo",
            "score_risco_meta": "Risco de Meta",
            "score_geral_risco": "Score Geral"
        })
    )

    mapa_risco_melt = mapa_risco.melt(id_vars="regiao_pred", var_name="Indicador", value_name="Risco")

    grafico_heatmap = px.density_heatmap(
        mapa_risco_melt,
        x="Indicador",
        y="regiao_pred",
        z="Risco",
        histfunc="avg",
        text_auto=".1%",
        title="Heatmap de risco por região",
        labels={"regiao_pred": "Região", "Risco": "Nível de risco"}
    )
    exibir_grafico(grafico_heatmap, use_container_width=True)

    st.markdown("---")
    st.subheader("5. Simulador de redução de desconto")
    st.write("Simulação simples para estimar o ganho de lucro caso o desconto médio seja reduzido.")

    desconto_atual = base_preditiva_filtrada["desconto_pct_pred"].mean()

    novo_desconto = st.slider(
        "Novo desconto médio simulado (%)",
        min_value=0.0,
        max_value=float(max(25, round(desconto_atual + 5, 1))),
        value=float(round(max(desconto_atual - 5, 0), 1)),
        step=0.5
    )

    receita_total = base_preditiva_filtrada["receita_pred"].sum()
    lucro_total = base_preditiva_filtrada["lucro_pred"].sum()

    desconto_atual_decimal = desconto_atual / 100
    novo_desconto_decimal = novo_desconto / 100

    if desconto_atual_decimal < 1:
        receita_bruta_estimada = receita_total / (1 - desconto_atual_decimal)
    else:
        receita_bruta_estimada = receita_total

    receita_simulada = receita_bruta_estimada * (1 - novo_desconto_decimal)
    ganho_estimado = receita_simulada - receita_total
    lucro_simulado = lucro_total + ganho_estimado

    margem_atual = dividir_seguro(lucro_total, receita_total) * 100
    margem_simulada = dividir_seguro(lucro_simulado, receita_simulada) * 100

    col_sim1, col_sim2, col_sim3 = st.columns(3)

    with col_sim1:
        exibir_card_kpi("Ganho estimado", formatar_moeda(ganho_estimado), "Estimativa de ganho com redução do desconto.", status="positivo" if ganho_estimado > 0 else "critico")
    with col_sim2:
        exibir_card_kpi("Margem atual", formatar_percentual(margem_atual), "Margem observada nos filtros selecionados.", status="critico" if margem_atual < LIMITE_MINIMO_MARGEM else "positivo")
    with col_sim3:
        exibir_card_kpi("Margem simulada", formatar_percentual(margem_simulada), "Margem estimada após ajuste do desconto.", status="critico" if margem_simulada < LIMITE_MINIMO_MARGEM else "positivo")

    st.info(
        f"Com os filtros selecionados, o desconto médio atual é de "
        f"{formatar_percentual(desconto_atual)}. Ao simular um desconto médio de "
        f"{formatar_percentual(novo_desconto)}, o ganho estimado é de "
        f"{formatar_moeda(ganho_estimado)}."
    )



# =========================
# EXECUÇÃO DO DASHBOARD
# =========================

aplicar_estilo_dashboard()
base = carregar_dados()
base_filtrada = base.copy()

exibir_topo_dashboard()

paginas_dashboard = [
    "Visão Geral",
    "Vendas e Comercial",
    "Análise Regional",
    "Análise de Produtos",
    "Diagnóstico Preditivo Comercial"
]

pagina = st.radio(
    "Selecione a página",
    paginas_dashboard,
    horizontal=True
)

if pagina == "Visão Geral":
    pagina_visao_geral(base_filtrada)

elif pagina == "Vendas e Comercial":
    pagina_vendas_comercial(base_filtrada)

elif pagina == "Análise Regional":
    pagina_analise_regional(base_filtrada)

elif pagina == "Análise de Produtos":
    pagina_analise_produtos(base_filtrada)

elif pagina == "Diagnóstico Preditivo Comercial":
    pagina_diagnostico_preditivo(base_filtrada)
