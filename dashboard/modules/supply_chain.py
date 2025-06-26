import streamlit as st
import pandas as pd
import base64
from utils import load_csv, apply_responsive
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go

def show_tab1(df):
    st.markdown("### Carte des Fournisseurs les Plus Fiables")

    # Moyenne du Resilience_Index par pays
    df_resilience = df.groupby("supplier_country", as_index=False)["Resilience_Index"].mean()

    fig_map = px.choropleth(
        df_resilience,
        locations="supplier_country",
        locationmode="country names",
        color="Resilience_Index",
        color_continuous_scale="Greens"
    )
    fig_map.update_geos(showcountries=True, showcoastlines=True, fitbounds="locations")
    st.plotly_chart(apply_responsive(fig_map), use_container_width=True)

    # TOP pays
    st.markdown("### Top 10 des Pays avec les Fournisseurs les Plus Fiables")
    top_countries_best = (
        df.groupby('supplier_country', as_index=False)['Resilience_Index']
        .mean()
        .sort_values(by='Resilience_Index', ascending=False)
        .head(10)
    )
    st.dataframe(top_countries_best, use_container_width=True, hide_index=True)

    st.markdown("### Top 10 des Pays avec les Fournisseurs les Moins Fiables")
    top_countries_worst = (
        df.groupby('supplier_country', as_index=False)['Resilience_Index']
        .mean()
        .sort_values(by='Resilience_Index', ascending=True)
        .head(10)
    )
    st.dataframe(top_countries_worst, use_container_width=True, hide_index=True)

    # Distributions
    st.markdown("### Distribution des Scores")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Risk Score")
        fig_risk = px.histogram(df, x="Risk_Score", nbins=50, color_discrete_sequence=["#e74c3c"])
        st.plotly_chart(apply_responsive(fig_risk), use_container_width=True)

    with col2:
        st.subheader("Indice de Résilience")
        fig_resilience = px.histogram(df, x="Resilience_Index", nbins=50, color_discrete_sequence=["#27ae60"])
        st.plotly_chart(apply_responsive(fig_resilience), use_container_width=True)

def show_tab2(df):
    # --- Analyse des Délais ---
    st.markdown("### Analyse des Délais de Livraison")
    
    fig_lead_hist = px.histogram(df, x="lead_time_days", nbins=50, color_discrete_sequence=["#1f77b4"])
    st.plotly_chart(apply_responsive(fig_lead_hist), use_container_width=True)

    top_lead_time_long = (
        df.groupby("supplier_country", as_index=False)["lead_time_days"]
        .mean()
        .sort_values(by="lead_time_days", ascending=False)
        .head(10)
    )
    st.markdown("Top 10 des Pays avec les Délais Moyens les Plus Longs")
    st.dataframe(top_lead_time_long, use_container_width=True, hide_index=True)

    top_lead_time_short = (
        df.groupby("supplier_country", as_index=False)["lead_time_days"]
        .mean()
        .sort_values(by="lead_time_days", ascending=True)
        .head(10)
    )
    st.markdown("Top 10 des Pays avec les Meilleurs Délais Moyens")
    st.dataframe(top_lead_time_short, use_container_width=True, hide_index=True)

    # --- Analyse des Retards ---
    st.markdown("### Analyse des Retards de Livraison (Delivery Time Deviation)")

    fig_delay_hist = px.histogram(df, x="delivery_time_deviation", nbins=50, color_discrete_sequence=["#ff7f0e"])
    st.plotly_chart(apply_responsive(fig_delay_hist), use_container_width=True)

    # KPIs retards / avances
    n_total = len(df)
    n_retard = (df['delivery_time_deviation'] > 0).sum()
    n_avance = (df['delivery_time_deviation'] < 0).sum()
    st.markdown(f"**Proportion de retards :** {n_retard / n_total * 100:.2f}%")
    st.markdown(f"**Proportion d'avances :** {n_avance / n_total * 100:.2f}%")

    # Boxplot des retards pour les pays les plus représentés
    st.markdown("### Distribution des Retards de Livraison par Pays (Top 10)")
    top_countries = df['supplier_country'].value_counts().head(10).index.tolist()
    df_top_countries = df[df['supplier_country'].isin(top_countries)]

    fig_box = px.box(
        df_top_countries,
        x="supplier_country",
        y="delivery_time_deviation",
        color="supplier_country",
        category_orders={"supplier_country": top_countries}
    )
    st.plotly_chart(apply_responsive(fig_box), use_container_width=True)

    # --- Fournisseurs les Plus et Moins Résilients ---
    st.markdown("### Top 10 des Fournisseurs les Plus Résilients")
    top_suppliers_best = (
        df.groupby(['supplier_id', 'supplier_country'], as_index=False)['Resilience_Index']
        .mean()
        .sort_values(by='Resilience_Index', ascending=False)
        .head(10)
    )
    st.dataframe(top_suppliers_best, use_container_width=True, hide_index=True)

    st.markdown("### Top 10 des Fournisseurs les Moins Résilients")
    top_suppliers_worst = (
        df.groupby(['supplier_id', 'supplier_country'], as_index=False)['Resilience_Index']
        .mean()
        .sort_values(by='Resilience_Index', ascending=True)
        .head(10)
    )
    st.dataframe(top_suppliers_worst, use_container_width=True, hide_index=True)

    # --- Analyse par Catégorie de Risque ---
    if 'risk_classification' in df.columns:
        st.markdown("### Analyse par Catégorie de Risque")
        risk_summary = (
            df.groupby('risk_classification')
            .agg({
                'Risk_Score': 'mean',
                'lead_time_days': 'mean',
                'product_id': 'count'
            })
            .rename(columns={'product_id': 'Nombre de Produits'})
            .reset_index()
        )
        st.dataframe(risk_summary, use_container_width=True, hide_index=True)

def show_tab3(df):
    st.markdown("### Matrice de Corrélation")

    # Colonnes pertinentes à corréler
    corr_cols = [
        'Risk_Score',
        'Resilience_Index',
        'lead_time_days',
        'delay_probability',
        'disruption_likelihood_score',
        'supplier_reliability_score',
        'delivery_time_deviation'
    ]

    # Calcul de la matrice
    corr_matrix = df[corr_cols].corr().round(2)

    # Plotly Heatmap stylée
    fig = go.Figure(
        data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            colorscale='YlGnBu',
            zmin=-1,
            zmax=1,
            text=corr_matrix.values,
            texttemplate="%{text}",
            hovertemplate="Corr(%{x}, %{y}) = %{z}<extra></extra>",
            colorbar=dict(title="Corrélation")
        )
    )

    fig.update_layout(
        xaxis_title="Variables",
        yaxis_title="Variables",
        margin=dict(l=40, r=40, t=50, b=40)
    )

    st.plotly_chart(apply_responsive(fig), use_container_width=True)

def show():
    # Charger l'icône et encoder en base64
    with open("assets/supply_chain_icon.png", "rb") as f:
        icon_base64 = base64.b64encode(f.read()).decode()

    # Titre + Icône alignés
    st.markdown(
        f"""
        <div style="display: flex; align-items: center;">
            <img src="data:image/png;base64,{icon_base64}" alt="Icone" style="width:60px; margin-right: 10px;">
            <h1 style="margin: 0;">Analyse de Risque — Fournisseurs & Résilience Logistique</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("""
    ### Contexte et Source des Données

    Ce module repose sur le dataset **[Supply Chain Dataset – Natasha (Kaggle)](https://www.kaggle.com/datasets/natasha0786/supply-chain-dataset/data)** :
    - **Domaine :** Logistique et chaîne d’approvisionnement  
    - **Format :** CSV (113 000 lignes)  
    - **Description :** Vue complète des opérations de la chaîne logistique, enrichie par des indicateurs opérationnels (stocks, coûts, équipements, fiabilité fournisseurs) et contextuels (risques, perturbations, retards, délais de douane).
    - **Pourquoi ce choix ?** : Permet d’identifier les vulnérabilités logistiques, d’évaluer la résilience des fournisseurs, et de construire des indicateurs fiables pour l’analyse de risques.

    **Le `Risk_Score` est une moyenne pondérée de :**
    - `route_risk_level` (normalisé /10)  
    - `disruption_likelihood_score`  
    - `delay_probability`  
    - `delivery_time_deviation` (normalisé /10)

    **L’indice de résilience (`Resilience_Index`)** est défini comme suit :  
    > `supplier_reliability_score × (1 - Risk_Score)`
    """)

    # Charger les données nettoyées
    df = load_csv("../data/cleaned/supply_chain_cleaned.csv")

    # Aperçu dans un expander
    with st.expander("Voir un aperçu du dataset (1000 lignes)"):
        st.dataframe(df.head(1000))

    # KPI globaux
    st.markdown("### Indicateurs Clés Globaux")

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Produits", df['product_id'].nunique())
    col2.metric("Fournisseurs", df['supplier_id'].nunique())
    col3.metric("Pays Fournisseurs", df['supplier_country'].nunique())
    col4.metric("Risk Score (moy)", f"{df['Risk_Score'].mean():.3f}")
    col5.metric("Résilience (moy)", f"{df['Resilience_Index'].mean():.3f}")

    tab1, tab2, tab3 = st.tabs(["Vue Globale", "Analyses Plage Temporelle", "Heatmap"])

    with tab1:
        show_tab1(df)

    with tab2:
        show_tab2(df)

    with tab3:
        show_tab3(df)

    # Résumé
    st.info(f"""
    **Résumé :**
    - Fournisseurs analysés : {df['supplier_id'].nunique():,} répartis sur {df['supplier_country'].nunique()} pays.
    - Produits couverts : {df['product_id'].nunique():,}
    - Risk Score moyen : {df['Risk_Score'].mean():.3f}  
    - Résilience moyenne : {df['Resilience_Index'].mean():.3f}
    - Délais > 5 jours : {(df['lead_time_days'] > 5).mean() * 100:.2f}% des cas
    - Retards (delivery_time_deviation > 0) : {(df['delivery_time_deviation'] > 0).mean() * 100:.2f}% des livraisons
    """)