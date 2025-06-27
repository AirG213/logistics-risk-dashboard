import streamlit as st
import base64
import pandas as pd
import base64
from utils import load_csv, apply_responsive
import plotly.express as px

def show_tab1(df):

    st.subheader("Répartition par Type d’Accident")
    type_counts = df["Accident Type"].value_counts().reset_index()
    type_counts.columns = ["Accident Type", "Count"]
    fig_type = px.bar(
        type_counts,
        x="Accident Type",
        y="Count",
        color="Accident Type",
        title="Nombre d'incidents par type",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    st.plotly_chart(apply_responsive(fig_type), use_container_width=True)

    st.markdown("### Moyennes des Variables par Type d’Accident")
    st.markdown("**Comparaison des indicateurs selon le type d’accident**")
    variables = [
        "Total Damage Cost", "Total Persons Killed", "Total Persons Injured",
        "Hazmat Cars", "Hazmat Cars Damaged", "Persons Evacuated"
    ]
    selected_vars = st.multiselect(
        "Variables à afficher :",
        options=variables,
        default=["Total Damage Cost"]
    )
    if selected_vars:
        df_avg = df.groupby("Accident Type")[selected_vars].mean().reset_index()
        for var in selected_vars:
            st.markdown(f"#### {var}")
            sorted_df = df_avg.sort_values(var, ascending=False)
            fig = px.bar(
                sorted_df,
                x=var,
                y="Accident Type",
                orientation="h",
                height=400,
                color_discrete_sequence=["#2ecc71"]
            )
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Veuillez sélectionner au moins une variable.")

    st.subheader("Niveau de Criticité Global")
    crit_counts = df["Niveau_criticité"].value_counts().reset_index()
    crit_counts.columns = ["Niveau_criticité", "Count"]
    fig_crit = px.pie(
        crit_counts,
        names="Niveau_criticité",
        values="Count",
        title="Répartition du niveau de criticité",
        color="Niveau_criticité",
        color_discrete_map={"Low": "green", "Medium": "orange", "High": "red"}
    )
    st.plotly_chart(apply_responsive(fig_crit), use_container_width=True)

    st.subheader("Carte des Incidents")
    # Nettoyage des coordonnées
    df_map = df.dropna(subset=["Latitude", "Longitude"])
    df_map = df_map[
        (df_map["Latitude"].between(24.5, 49.5)) &
        (df_map["Longitude"].between(-125, -66))
    ]

    fig_map = px.scatter_mapbox(
        df_map,
        lat="Latitude",
        lon="Longitude",
        color="Niveau_criticité",
        zoom=3,
        height=600,
        mapbox_style="carto-positron",
        color_discrete_map={
            "Low": "#2ecc71",
            "Medium": "#f1c40f",
            "High": "#e74c3c"
        },
        hover_data=["State Name", "County Name", "Accident Type", "Total Damage Cost", "Total Persons Killed"],
    )

    fig_map.update_layout(
        margin={"r":0, "t":0, "l":0, "b":0},
        mapbox_center={"lat": 37.5, "lon": -95},
        mapbox_zoom=3.2
    )

    st.plotly_chart(apply_responsive(fig_map), use_container_width=True)

    st.subheader("Comtés les plus et les moins touchés")
    county_counts = df["County Name"].value_counts().reset_index()
    county_counts.columns = ["County", "Count"]
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Top 10 — Comtés les plus touchés**")
        st.dataframe(county_counts.head(10), use_container_width=True)

    with col2:
        st.markdown("**Top 10 — Comtés les moins touchés (≥1 incident)**")
        st.dataframe(county_counts[county_counts["Count"] > 0].tail(10), use_container_width=True)


def show_tab2(df):
    st.subheader("Évolution des Incidents Ferroviaires sur les 20 dernières années")

    # Par année
    incidents_by_year = df["Report Year"].value_counts().sort_index()
    fig_years = px.bar(
        x=incidents_by_year.index,
        y=incidents_by_year.values,
        labels={"x": "Année", "y": "Nombre d'incidents"},
        title="Nombre d'incidents par année"
    )
    st.plotly_chart(fig_years, use_container_width=True)

    # Répartition par type d'incident sur le temps
    st.subheader("Types d'Accidents au Fil du Temps")
    type_year = df.groupby(["Report Year", "Accident Type"]).size().unstack(fill_value=0)
    fig_type = px.area(
        type_year,
        labels={"value": "Nombre", "Report Year": "Année", "variable": "Type"},
        title="Évolution des types d'accidents"
    )
    st.plotly_chart(fig_type, use_container_width=True)

    # Risque moyen par année
    st.subheader("Évolution du Risque Composite Moyen")
    risk_by_year = df.groupby("Report Year")["Risque_composite"].mean()
    fig_risk = px.line(
        x=risk_by_year.index,
        y=risk_by_year.values,
        markers=True,
        labels={"x": "Année", "y": "Risque moyen"},
        title="Risque moyen par année"
    )
    st.plotly_chart(fig_risk, use_container_width=True)

    # Moment de la journée
    st.subheader("Répartition par Moment de la Journée")
    fig_time = px.histogram(
        df,
        x="TimeOfDay",
        color="Niveau_criticité",
        barmode="group",
        category_orders={"TimeOfDay": ["EARLY MORNING", "LATE MORNING", "AFTERNOON", "EVENING", "DARK", "DAWN"]},
        labels={"count": "Nombre d'incidents"},
        title="Incidents par moment de la journée"
    )
    st.plotly_chart(fig_time, use_container_width=True)


def show_tab3(df):
    st.subheader("Analyse de Corrélation — Variables d'Impact")

    general_cols = [
        "Total Damage Cost", "Total Persons Killed", "Total Persons Injured",
        "Hazmat Cars", "Hazmat Cars Damaged", "Persons Evacuated", "Risque_composite"
    ]

    st.markdown("### Corrélation Générale")
    st.markdown("**Corrélation entre les variables générales**")
    corr_general = df[general_cols].corr()
    fig1 = px.imshow(corr_general, text_auto=True, color_continuous_scale="RdBu_r", aspect="auto")
    fig1.update_layout(width=900, height=600, margin=dict(l=50, r=50, t=50, b=50))
    st.plotly_chart(fig1, use_container_width=True)
    st.caption("Les variables fortement corrélées sont les blessures, les décès et les coûts matériels. Hazmat reste faiblement lié.")

    st.markdown("### Corrélation Hazmat & Risque")
    st.markdown("**Corrélation Hazmat et Risque Composite**")
    hazmat_cols = ["Hazmat Cars", "Hazmat Cars Damaged", "Persons Evacuated", "Risque_composite"]
    corr_hazmat = df[hazmat_cols].corr()
    fig2 = px.imshow(corr_hazmat, text_auto=True, color_continuous_scale="YlGnBu", aspect="auto")
    fig2.update_layout(width=800, height=500, margin=dict(l=50, r=50, t=50, b=50))
    st.plotly_chart(fig2, use_container_width=True)
    st.caption("Corrélation modérée entre wagons Hazmat endommagés et nombre total. Risque composite peu influencé ici.")

def show():
    # Charger l'icône et encoder en base64
    with open("assets/railroad_icon.png", "rb") as f:
        icon_base64 = base64.b64encode(f.read()).decode()

    # Titre + Icône alignés
    st.markdown(
        f"""
        <div style="display: flex; align-items: center;">
            <img src="data:image/png;base64,{icon_base64}" alt="Icone" style="width:60px; margin-right: 10px;">
            <h1 style="margin: 0;">Analyse de Risque — Transport Ferroviaire</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("""
    ### Contexte et Source des Données
    Ce module repose sur le dataset **[Railroad Accident/Incident Data – Kaggle](https://www.kaggle.com/datasets/chrico03/railroad-accident-and-incident-data)** :
    - **Domaine :** Transport ferroviaire américain  
    - **Format :** CSV (nettoyé)  
    - **Description :** Plus de 60 000 rapports d’incidents (déraillements, collisions, feux, etc.), incluant type d'accident, état, nombre de personnes concernées, durée, dommages, et coordonnées géographiques.
    - **Pourquoi ce choix ?** : Permet de détecter les zones ferroviaires critiques et d’analyser les types d’incidents impactant la chaîne logistique lourde.

    **Périmètre de l’étude :**
    - L’analyse couvre uniquement les **20 dernières années** (2002–2022) sur la base de la colonne `Report Year`
    - Les enregistrements antérieurs (jusqu’à 1975) ont été **exclus** de l’étude

    **Le `Risque_composite`** est un indicateur calculé à partir de :
    - la fréquence de l’incident  
    - la gravité de ses conséquences (victimes, dégâts)  
    - le niveau d'évacuation ou impact Hazmat  

    > Les valeurs sont normalisées pour aboutir à un `Niveau_criticité` qualitatif : Faible / Moyen / Élevé.
    """)

    # Charger les données nettoyées
    df = load_csv("../data/cleaned/railroad_accident_cleaned.csv")
    
    # Nettoyage des noms de colonnes (strip des espaces invisibles s’il y en a)
    df.columns = df.columns.str.strip()

    # Créer une colonne Date complète à partir des 3 colonnes séparées
    df["Accident_Date"] = pd.to_datetime({
        "year": df["Report Year"],
        "month": df["Accident Month"],
        "day": df["Day"]
    }, errors="coerce")

    # Aperçu dans un expander
    with st.expander("Voir un aperçu du dataset (1000 lignes)"):
        st.dataframe(df.head(1000))

    # KPI globaux
    st.markdown("### Indicateurs Clés Globaux")

    total_incidents = df.shape[0]
    total_killed = df["Total Persons Killed"].sum()
    total_injured = df["Total Persons Injured"].sum()
    total_damage = df["Total Damage Cost"].sum()
    avg_damage = df["Total Damage Cost"].mean()
    max_damage_state = df.groupby("State Name")["Total Damage Cost"].sum().idxmax()
    top_state = df["State Name"].value_counts().idxmax()

    col1, col2, col3 = st.columns(3)
    col1.metric("Incidents Totaux", f"{total_incidents:,}")
    col2.metric("Personnes Tuées", f"{total_killed:,}")
    col3.metric("Personnes Blessées", f"{total_injured:,}")

    col4, col5, col6 = st.columns(3)
    col4.metric("Dommages Totaux", f"${total_damage:,.0f}")
    col5.metric("Dommage Moyen", f"${avg_damage:,.0f}")
    col6.metric("État + Touché ($)", max_damage_state)

    tab1, tab2, tab3 = st.tabs(["Vue Globale", "Analyses Temporelle", "Heatmap"])

    with tab1:
        show_tab1(df)

    with tab2:
        show_tab2(df)

    with tab3:
        show_tab3(df)


    # Résumé
    st.info(f"""
    **Résumé Général des Incidents Ferroviaires :**

    - **Nombre total d'incidents :** {total_incidents:,}
    - **Total de personnes tuées :** {total_killed:,}
    - **Total de personnes blessées :** {total_injured:,}
    - **Coût total des dommages :** ${total_damage:,.0f}
    - **État le plus touché :** {top_state}  
    ↳ Dommages cumulés : ${df[df['State Name'] == top_state]['Total Damage Cost'].sum():,.0f}
    - **Coût moyen par incident :** ${avg_damage:,.0f}
    - **Année la plus critique :** {df['Report Year'].mode()[0]}  
    ↳ Nombre d’incidents : {df['Report Year'].value_counts().max()}
    - **Risque composite moyen :** {df['Risque_composite'].mean():.2e}  
    ↳ (Score faible car basé sur 210M trajets)
    - **Niveau de criticité dominant :** {df['Niveau_criticité'].mode()[0]}
    """)