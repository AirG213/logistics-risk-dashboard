import streamlit as st
import plotly.express as px
import pandas as pd
import base64

def get_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

icon_base64 = get_base64("assets/traffic_accident_icon.png")

@st.cache_data
def load_clean_data():
    df = pd.read_csv("../data/cleaned/usa_accidents_traffic_cleaned.csv")
    df['Start_Time'] = pd.to_datetime(df['Start_Time'])
    df['HourOfDay'] = df['Start_Time'].dt.hour
    df['DayOfWeek'] = df['Start_Time'].dt.dayofweek
    df['Month'] = df['Start_Time'].dt.month
    return df

@st.cache_data
def prepare_data(df):
    hour_counts = df['HourOfDay'].value_counts().sort_index().reset_index()
    hour_counts.columns = ['HourOfDay', 'Count']

    day_counts = df['DayOfWeek'].value_counts().sort_index().reset_index()
    day_counts.columns = ['DayOfWeek', 'Count']

    month_counts = df['Month'].value_counts().sort_index().reset_index()
    month_counts.columns = ['Month', 'Count']

    hour_scores = df.groupby('HourOfDay')['Risk_Score'].mean().reset_index()
    day_scores = df.groupby('DayOfWeek')['Risk_Score'].mean().reset_index()
    month_scores = df.groupby('Month')['Risk_Score'].mean().reset_index()

    risk_summary = df['Risk_Category'].value_counts().reset_index()
    risk_summary.columns = ['Risk_Category', 'Count']
    risk_summary['Proportion (%)'] = (risk_summary['Count'] / df.shape[0] * 100).round(2)

    heatmap_data = df[df['Risk_Category'].isin(['Peak Hour Congestion', 'Weather Disruption'])]
    heatmap_data = heatmap_data[heatmap_data['Main_Weather'].isin(['Rain', 'Snow', 'Fog', 'Thunderstorm'])]
    heatmap = heatmap_data.groupby(['Main_Weather', 'HourOfDay'])['Risk_Score'].mean().reset_index()

    return hour_counts, day_counts, month_counts, hour_scores, day_scores, month_scores, risk_summary, heatmap

def apply_responsive(fig):
    fig.update_layout(
        autosize=True,
        width=None,
        height=500,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    return fig

def show():
    # Titre + Icône alignés
    st.markdown(
        f"""
        <div style="display: flex; align-items: center;">
            <img src="data:image/png;base64,{icon_base64}" alt="Icone" style="width:60px; margin-right: 10px;">
            <h1 style="margin: 0;">Analyse de Risque — Transport Routier</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Charger les données
    df = load_clean_data()

    st.markdown("""
    ### Contexte et Source des Données

    Ce module est basé sur le dataset **[US Accidents (2016–2023)](https://www.kaggle.com/datasets/sobhanmoosavi/us-accidents)** :
    - **Domaine :** Transport routier (USA)
    - **Format :** CSV
    - **Description :** 7,7 millions de rapports d'accidents réels aux États-Unis, de 2016 à 2023, incluant gravité, durée, impact sur le trafic et coordonnées GPS.
    - **Pourquoi ce choix ?** : Fournit une base solide pour estimer la probabilité de perturbations routières, dans le cadre de l'analyse de résilience logistique.

    **Le Risk_Score a été calculé comme suit :**
    Chaque incident est évalué selon trois critères :
    - Gravité (`Severity`) normalisée de 1 à 4.
    - Durée normalisée.
    - Facteur météo pondéré (pluie, neige, orage, brouillard).

    Ces critères pondérés donnent un `Risk_Score` de 0 (nul) à 1 (élevé).
    """)

    # Aperçu du CSV
    with st.expander("Voir un aperçu du fichier final nettoyé et enrichi (100000 lignes)"):
        st.dataframe(df.head(100000))

    # Préparer les agrégats
    hour_counts, day_counts, month_counts, hour_scores, day_scores, month_scores, risk_summary, heatmap = prepare_data(df)

    # KPI
    total = df.shape[0]
    peak_hour_pct = (df[df['Risk_Category'] == 'Peak Hour Congestion'].shape[0] / total) * 100
    infra_block_mean = df[df['Risk_Category'] == 'High Infrastructure Block']['Duration(min)'].mean()
    weather_pct = (df[df['Risk_Category'] == 'Weather Disruption'].shape[0] / total) * 100

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Heures de pointe", f"{peak_hour_pct:.1f} %")
    col2.metric("Durée Blocage Moyenne", f"{infra_block_mean:.0f} min")
    col3.metric("Perturbations Météo", f"{weather_pct:.1f} %")
    col4.metric("Total Accidents", f"{total:,}")

    # TABS pour structurer la page
    tab1, tab2, tab3 = st.tabs(["Vue Globale", "Analyses Plage Temporelle", "Heatmap"])

    with tab1:
        st.subheader("Répartition des Catégories de Risque")
        fig_cat = px.bar(
            risk_summary,
            x='Count',
            y='Risk_Category',
            orientation='h',
            text='Proportion (%)',
            color='Risk_Category',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        st.plotly_chart(apply_responsive(fig_cat), use_container_width=True)

    with tab2:
        st.subheader("Analyse par Heure de la Journée")
        fig_hour_count = px.bar(hour_counts, x='HourOfDay', y='Count')
        st.plotly_chart(apply_responsive(fig_hour_count), use_container_width=True)

        fig_hour_score = px.line(hour_scores, x='HourOfDay', y='Risk_Score', markers=True)
        st.plotly_chart(apply_responsive(fig_hour_score), use_container_width=True)

        st.subheader("Analyse par Jour de la Semaine")
        fig_day_count = px.bar(day_counts, x='DayOfWeek', y='Count')
        st.plotly_chart(apply_responsive(fig_day_count), use_container_width=True)

        fig_day_score = px.line(day_scores, x='DayOfWeek', y='Risk_Score', markers=True)
        st.plotly_chart(apply_responsive(fig_day_score), use_container_width=True)

        st.subheader("Analyse par Mois")
        fig_month_count = px.bar(month_counts, x='Month', y='Count')
        st.plotly_chart(apply_responsive(fig_month_count), use_container_width=True)

        fig_month_score = px.line(month_scores, x='Month', y='Risk_Score', markers=True)
        st.plotly_chart(apply_responsive(fig_month_score), use_container_width=True)

    with tab3:
        st.subheader("Heatmap Risk_Score (Météo vs Heure)")
        heatmap_pivot = heatmap.pivot(index='Main_Weather', columns='HourOfDay', values='Risk_Score')
        fig_heat = px.imshow(
            heatmap_pivot.values,
            labels=dict(x="Heure", y="Météo", color="Risk_Score"),
            x=heatmap_pivot.columns,
            y=heatmap_pivot.index,
            title="Heatmap Risque Moyen (Météo vs Heure)"
        )
        st.plotly_chart(apply_responsive(fig_heat), use_container_width=True)

    # Résumé
    st.info(f"""
    **Résumé du module :**
    - Heures de pointe : {peak_hour_pct:.1f}% des incidents contribuent directement à la congestion.
    - Incidents « High Infrastructure Block » : durée moyenne {infra_block_mean:.0f} minutes.
    - Perturbations météo : {weather_pct:.1f}% des cas (pluie, neige, brouillard).
    - Total incidents analysés : {total:,}.
    """)