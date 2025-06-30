import streamlit as st
import plotly.express as px
import pandas as pd
from utils import load_csv, apply_responsive, get_base64

def show(df_traffic, df_airline, df_railroad, df_shipping):
    st.title('Analyse de Risque - Résilience Chaîne Logistique')
    st.write("Ce tableau de bord interactif résume les incidents par mode de transport.")

    # Indicateurs Globaux
    st.markdown("### Vue d’ensemble des incidents")

    col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)

    col_kpi1.metric("🚗 Accidents Routiers", f"{len(df_traffic):,}")
    col_kpi2.metric("✈️ Retards Aériens", f"{int(df_airline['arr_del15'].sum()):,}")
    col_kpi3.metric("🚆 Accidents Ferroviaires", f"{len(df_railroad):,}")
    col_kpi4.metric("🚢 Accidents Maritimes", f"{len(df_shipping):,}")

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
            color_discrete_sequence=px.colors.qualitative.Set1
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
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        st.plotly_chart(apply_responsive(fig_rail), use_container_width=True)

    with col4:
        st.markdown("### Transport Maritime")
        top_ship = (
            df_shipping[df_shipping["Acc_Type"] != "Other"]
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