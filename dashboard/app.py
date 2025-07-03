import streamlit as st
import plotly.express as px
from utils import load_csv, apply_responsive
from sidebar import show_sidebar
import pandas as pd

show_sidebar()

def show():
    df_traffic = load_csv("../data/cleaned/usa_accidents_traffic_cleaned.csv")
    df_airline = load_csv("../data/cleaned/airline_delay_cause_cleaned.csv")
    df_railroad = load_csv("../data/cleaned/railroad_accident_cleaned.csv")
    df_shipping = load_csv("../data/cleaned/shipping_accidents_cleaned.csv")

    st.title('Analyse de Risque - Résilience Chaîne Logistique')
    st.markdown("""
    La résilience des chaînes logistiques est devenue un enjeu stratégique face à la montée des risques : catastrophes naturelles, perturbations géopolitiques, défaillances techniques ou aléas climatiques.

    Ce tableau de bord interactif s'inscrit dans une démarche de recherche menée au CESI LINEACT, visant à développer un **système d'analyse des risques logistiques** basé sur les données.
    Il permet d'explorer les incidents critiques selon quatre modes de transport : **routier**, **aérien**, **ferroviaire** et **maritime**, à partir de jeux de données publics.

    L'objectif ? Fournir aux décideurs une visualisation claire des zones de fragilité, des typologies d'incidents, et des axes d'amélioration pour anticiper les perturbations et renforcer la résilience globale.

    ---
    """)
    # Indicateurs Globaux
    st.markdown("### Nombre Total d'Incidents par Mode de Transport")

    col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)

    col_kpi1.metric("🚗 Accidents Routiers", f"{len(df_traffic):,}")
    col_kpi2.metric("✈️ Retards Aériens", f"{int(df_airline['arr_del15'].sum()):,}")
    col_kpi3.metric("🚆 Accidents Ferroviaires", f"{len(df_railroad):,}")
    col_kpi4.metric("🚢 Accidents Maritimes", f"{len(df_shipping):,}")

    df_traffic['Start_Time'] = pd.to_datetime(df_traffic['Start_Time'])

    col_kpi1.metric('🚗 Plage Temporelle', f'{df_traffic['Start_Time'].min().year} - {df_traffic['Start_Time'].max().year}')
    col_kpi2.metric('✈️ Plage Temporelle', f'{df_airline['year'].min().astype(int)} - {df_airline['year'].max().astype(int)}')
    col_kpi3.metric('🚆 Plage Temporelle', f'{df_railroad['Report Year'].min().astype(int)} - {df_railroad['Report Year'].max().astype(int)}')
    col_kpi4.metric('🚢 Plage Temporelle', f'{df_shipping['Year'].min().astype(int)} - {df_shipping['Year'].max().astype(int)}')

    st.markdown("---")

    # Top Routier & Aérien
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Transport Routier")
        top_traffic = (
            df_traffic[df_traffic["Risk_Category"] != "Low Impact"]
            .value_counts(subset=["Risk_Category"])
            .reset_index(name="Nombre")
            .head(3)
        )
        fig_traf = px.bar(
            top_traffic,
            x="Nombre",
            y="Risk_Category",
            orientation="h",
            color="Risk_Category",
            title="Top 3 des catégories de risque",
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        st.plotly_chart(apply_responsive(fig_traf), use_container_width=True)

    with col2:
        st.markdown("### Transport Aérien")
        delay_cols_count = [
            'carrier_ct',
            'weather_ct',
            'nas_ct',
            'security_ct',
            'late_aircraft_ct'
        ]
        readable_labels_count = {
            'carrier_ct': 'Retard compagnie aérienne',
            'weather_ct': 'Retard météo',
            'nas_ct': 'Retard contrôle aérien (NAS)',
            'security_ct': 'Retard sécurité',
            'late_aircraft_ct': 'Retard avion précédent'
        }
        delay_counts = df_airline[delay_cols_count].sum().astype(int).reset_index()
        delay_counts.columns = ['Cause', 'Nombre de retards']
        delay_counts['Cause'] = delay_counts['Cause'].map(readable_labels_count)
        top_airline = delay_counts.sort_values("Nombre de retards", ascending=False).head(3)
        fig_air = px.bar(
            top_airline,
            x="Nombre de retards",
            y="Cause",
            orientation="h",
            color="Cause",
            text="Nombre de retards",
            title="Top 3 des causes de retard",
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        st.plotly_chart(apply_responsive(fig_air), use_container_width=True)

    # Top Ferroviaire & Maritime
    col3, col4 = st.columns(2)

    with col3:
        st.markdown("### Transport Ferroviaire")
        top_rail = (
            df_railroad[df_railroad["Accident Type"] != "Autre"]
            .value_counts(subset=["Accident Type"])
            .reset_index(name="Nombre")
            .head(3)
        )
        fig_rail = px.bar(
            top_rail,
            x="Nombre",
            y="Accident Type",
            orientation="h",
            color="Accident Type",
            title="Top 3 des types d'accident",
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        st.plotly_chart(apply_responsive(fig_rail), use_container_width=True)

    with col4:
        st.markdown("### Transport Maritime")
        top_ship = (
            df_shipping[df_shipping["Acc_Type"] != "Autre"]
            .value_counts(subset=["Acc_Type"])
            .reset_index(name="Nombre")
            .head(3)
        )
        fig_ship = px.bar(
            top_ship,
            x="Nombre",
            y="Acc_Type",
            orientation="h",
            color="Acc_Type",
            title="Top 3 des types d'accident",
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        st.plotly_chart(apply_responsive(fig_ship), use_container_width=True)

    st.markdown("---")
    st.info(f"""
    ### Explorer les Modules
    Chaque module propose ses propres indicateurs, visualisations spécifiques, et métriques de performance afin de mieux comprendre les vulnérabilités et leviers d'optimisation.
    Pour une analyse approfondie, **6 modules dédiés** sont accessibles via le menu :
    - 🚗 Transport Routier
    - ✈️ Transport Aérien
    - 🚆 Transport Ferroviaire
    - 🚢 Transport Maritime
    - 📦 Fournisseurs
    - 📬 Livraison Amazon
    """)

show()
