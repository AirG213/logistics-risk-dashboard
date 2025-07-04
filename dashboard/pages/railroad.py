import streamlit as st
import base64
import pandas as pd
import base64
from utils import load_csv, apply_responsive
import plotly.express as px
from sidebar import show_sidebar

show_sidebar()

def show_tab1(df):
    # Bloc 1 — Répartition par Type d'Accident
    st.subheader("Répartition par Type d'Accident")
    type_counts = df["Accident Type"].value_counts().reset_index()
    type_counts.columns = ["Type d'Accident", "Nombre d'incidents"]
    fig_type = px.bar(
        type_counts,
        x="Type d'Accident",
        y="Nombre d'incidents",
        color="Type d'Accident",
        title="Nombre d'incidents par type",
        color_discrete_sequence=px.colors.qualitative.Set3,
        labels={"Type d'Accident": "Type d'accident", "Nombre d'incidents": "Nombre d'incidents"}
    )
    st.plotly_chart(apply_responsive(fig_type), use_container_width=True)
    with st.expander("ℹ️ Comment lire ce graphique ?"):
        st.markdown("""
        Ce graphique montre combien d'incidents ont été enregistrés pour chaque **type d'accident ferroviaire**.  
        Il permet d'identifier les types les plus fréquents (ex. : **Déraillement**, **Collision**, etc.).
        """)
    st.markdown("---")

    # Bloc 2 — Moyennes des Variables par Type d'Accident
    st.markdown("### Moyennes des Indicateurs par Type d'Accident")
    st.markdown("**Comparaison des indicateurs selon le type d'accident**")
    variable_map = {
        "Total Damage Cost": "Coût Total des Dégâts",
        "Total Persons Killed": "Nombre de Morts",
        "Total Persons Injured": "Nombre de Blessés",
        "Hazmat Cars": "Wagons de matières dangereuses",
        "Hazmat Cars Damaged": "Wagons dangereux endommagés",
        "Persons Evacuated": "Personnes Évacuées"
    }
    variables = list(variable_map.keys())
    selected_vars = st.multiselect(
        "Variables à afficher :",
        options=variables,
        format_func=lambda x: variable_map.get(x, x),
        default=["Total Damage Cost"]
    )
    if selected_vars:
        df_avg = df.groupby("Accident Type")[selected_vars].mean().reset_index()
        for var in selected_vars:
            st.markdown(f"#### {variable_map[var]}")
            sorted_df = df_avg.sort_values(var, ascending=False)
            fig = px.bar(
                sorted_df,
                x=var,
                y="Accident Type",
                orientation="h",
                height=400,
                color_discrete_sequence=["#2ecc71"],
                labels={
                    var: variable_map[var],
                    "Accident Type": "Type d'accident"
                }
            )
            st.plotly_chart(apply_responsive(fig), use_container_width=True)

            with st.expander("ℹ️ Interprétation du graphique"):
                st.markdown(f"""
                Ce graphique montre la **moyenne de {variable_map[var]}** par type d'accident.  
                Il permet d'évaluer **l'impact moyen** de chaque type d'incident sur cette variable.
                """)
    else:
        st.info("Veuillez sélectionner au moins une variable.")

    st.markdown("---")

    # Bloc 3 — Niveau de Criticité Global
    st.subheader("Niveau de Criticité Global")
    crit_counts = df["Niveau_criticité"].value_counts().reset_index()
    crit_counts.columns = ["Niveau de Criticité", "Nombre"]
    fig_crit = px.pie(
        crit_counts,
        names="Niveau de Criticité",
        values="Nombre",
        title="Répartition du niveau de criticité",
        color="Niveau de Criticité",
        color_discrete_map={"Low": "green", "Medium": "orange", "High": "red"}
    )
    st.plotly_chart(apply_responsive(fig_crit), use_container_width=True)
    with st.expander("ℹ️ Que montre ce graphique ?"):
        st.markdown("""
        Cette répartition montre la **proportion d'incidents classés selon leur niveau de criticité**  
        (basé sur leur gravité, impact, dangerosité...).
        """)

    st.markdown("---")

    # Bloc 4 — Carte des Incidents
    st.subheader("Carte des Incidents Ferroviaires")
    df_map = df.dropna(subset=["Latitude", "Longitude"])
    df_map = df_map[
        (df_map["Latitude"].between(24.5, 49.5)) &
        (df_map["Longitude"].between(-125, -66))
    ]
    fig_map = px.scatter_map(
        df_map,
        lat="Latitude",
        lon="Longitude",
        color="Niveau_criticité",
        zoom=3,
        height=600,
        map_style="carto-positron",
        color_discrete_map={
            "Low": "#2ecc71",
            "Medium": "#f1c40f",
            "High": "#e74c3c"
        },
        hover_data={
            "State Name": True,
            "County Name": True,
            "Accident Type": True,
            "Total Damage Cost": True,
            "Total Persons Killed": True
        },
        labels={
            "State Name": "État",
            "County Name": "Comté",
            "Accident Type": "Type d'Accident",
            "Total Damage Cost": "Coût des Dégâts",
            "Total Persons Killed": "Personnes Décédées"
        }
    )
    fig_map.update_layout(
        margin={"r":0, "t":0, "l":0, "b":0},
        mapbox_center={"lat": 37.5, "lon": -95},
        mapbox_zoom=3.2
    )
    st.plotly_chart(apply_responsive(fig_map), use_container_width=True)

    st.markdown("---")

    # Bloc 5 — Comtés les plus et les moins touchés
    st.subheader("Comtés les Plus et Moins Touchés")
    county_counts = df["County Name"].value_counts().reset_index()
    county_counts.columns = ["Comté", "Nombre d'incidents"]
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Top 10 — Comtés les Plus Touchés**")
        st.dataframe(county_counts.head(10), use_container_width=True)
    with col2:
        st.markdown("**Top 10 — Comtés les Moins Touchés (≥1 incident)**")
        st.dataframe(county_counts[county_counts["Nombre d'incidents"] > 0].tail(10), use_container_width=True)
    with st.expander("📍 Que montre ce classement ?"):
        st.markdown("""
        Ces tableaux listent les **comtés les plus exposés aux incidents ferroviaires** (en nombre brut).  
        Cela permet d’identifier les **zones géographiques sensibles**.
        """)


def show_tab2(df):
    st.subheader("Évolution des Incidents Ferroviaires sur les 20 Dernières Années")

    # Bloc 1 — Incidents par Année
    incidents_by_year = df["Report Year"].value_counts().sort_index()
    fig_years = px.bar(
        x=incidents_by_year.index,
        y=incidents_by_year.values,
        labels={"x": "Année", "y": "Nombre d'incidents"},
        title="Nombre d'incidents par année"
    )
    st.plotly_chart(fig_years, use_container_width=True)

    with st.expander("📊 Que montre ce graphique ?"):
        st.markdown("""
        Ce graphique présente le **nombre total d'incidents enregistrés chaque année**.  
        Il permet d’identifier les années avec une augmentation ou diminution des accidents ferroviaires.
        """)

    st.markdown("---")

    # Bloc 2 — Types d'Accidents au Fil du Temps
    st.subheader("Types d'Accidents au Fil du Temps")
    type_year = df.groupby(["Report Year", "Accident Type"]).size().unstack(fill_value=0)
    fig_type = px.area(
        type_year,
        labels={"value": "Nombre d'incidents", "Report Year": "Année", "variable": "Type d'accident"},
        title="Évolution des types d'accidents"
    )
    st.plotly_chart(fig_type, use_container_width=True)

    with st.expander("📈 Interprétation de l'évolution des types d'accidents"):
        st.markdown("""
        Ce graphique **empilé** permet de visualiser comment la **répartition des types d'accidents**  
        a évolué au fil des années.  
        Il met en évidence les types dominants à chaque époque.
        """)

    st.markdown("---")

    # Bloc 3 — Risque Composite Moyen par Année
    st.subheader("Évolution du Risque Composite Moyen")
    risk_by_year = df.groupby("Report Year")["Risque_composite"].mean()
    fig_risk = px.line(
        x=risk_by_year.index,
        y=risk_by_year.values,
        markers=True,
        labels={"x": "Année", "y": "Risque Composite Moyen"},
        title="Risque moyen par année"
    )
    st.plotly_chart(fig_risk, use_container_width=True)

    with st.expander("📉 Que représente ce risque composite ?"):
        st.markdown("""
        Ce graphique montre la **moyenne annuelle du score de risque composite**,  
        qui agrège plusieurs indicateurs de dangerosité (coût, gravité, victimes…).  
        Une tendance haussière peut indiquer des incidents plus graves.
        """)

    st.markdown("---")

    # Bloc 4 — Moment de la Journée
    st.subheader("Répartition des Incidents par Moment de la Journée")

    ordre_fr = ["Tôt le matin", "Fin de matinée", "Après-midi", "Soirée"]

    fig_time = px.histogram(
        df,
        x="TimeOfDay",
        color="Niveau_criticité",
        barmode="group",
        category_orders={"TimeOfDay": ordre_fr},
        color_discrete_map={
            "Low": "#2ecc71",
            "Medium": "#f39c12",
            "High": "#e74c3c"
        },
        labels={
            "TimeOfDay": "Moment de la Journée",
            "count": "Nombre d'incidents",
            "Niveau_criticité": "Criticité"
        },
        title="Incidents par moment de la journée"
    )
    st.plotly_chart(apply_responsive(fig_time), use_container_width=True)

    with st.expander("🕓 Explication des moments de la journée"):
        st.markdown("""
        Ce graphique montre comment se répartissent les incidents ferroviaires selon le **moment de la journée** :  
        - **Tôt le matin**  
        - **Fin de matinée**  
        - **Après-midi**  
        - **Soirée**  

        Les couleurs indiquent le **niveau de criticité** de chaque incident.
        """)


def show_tab3(df):
    st.subheader("Analyse de Corrélation — Variables d'Impact")
    general_cols = [
        "Total Damage Cost", "Total Persons Killed", "Total Persons Injured",
        "Hazmat Cars", "Hazmat Cars Damaged", "Persons Evacuated", "Risque_composite"
    ]
    # Mapping des labels pour affichage FR
    label_map = {
        "Total Damage Cost": "Coût Matériel Total",
        "Total Persons Killed": "Nombre de Morts",
        "Total Persons Injured": "Nombre de Blessés",
        "Hazmat Cars": "Wagons de Matières Dangereuses",
        "Hazmat Cars Damaged": "Wagons de Matières Dangereuses Endommagés",
        "Persons Evacuated": "Personnes Évacuées",
        "Risque_composite": "Risque Composite"
    }
    # Corrélation générale
    st.markdown("### Corrélation Générale")
    corr_general = df[general_cols].corr()
    corr_general.index = corr_general.index.to_series().replace(label_map)
    corr_general.columns = corr_general.columns.to_series().replace(label_map)
    fig1 = px.imshow(
        corr_general,
        text_auto=True,
        color_continuous_scale="RdBu_r",
        aspect="auto",
        labels=dict(color="Corrélation")
    )
    fig1.update_layout(width=900, height=600, margin=dict(l=50, r=50, t=50, b=50))
    st.plotly_chart(fig1, use_container_width=True)
    with st.expander("📘 Comment lire cette matrice ?"):
        st.markdown("""
        Cette matrice montre la **corrélation linéaire** entre les variables générales.  
        - Une valeur proche de **1** (rouge foncé) indique une **forte corrélation positive** (les deux variables augmentent ensemble).  
        - Une valeur proche de **-1** (bleu foncé) indique une **forte corrélation négative** (l'une augmente quand l'autre diminue).  
        - Une valeur proche de **0** signifie **aucune corrélation linéaire**.
        """)

    st.markdown("---")

    # Corrélation Hazmat
    st.markdown("### Corrélation Matières Dangereuses & Risque")
    hazmat_cols = [
        "Hazmat Cars", "Hazmat Cars Damaged", "Persons Evacuated", "Risque_composite"
    ]
    corr_hazmat = df[hazmat_cols].corr()
    corr_hazmat.index = corr_hazmat.index.to_series().replace(label_map)
    corr_hazmat.columns = corr_hazmat.columns.to_series().replace(label_map)
    fig2 = px.imshow(
        corr_hazmat,
        text_auto=True,
        color_continuous_scale="YlGnBu",
        aspect="auto",
        labels=dict(color="Corrélation")
    )
    fig2.update_layout(width=800, height=500, margin=dict(l=50, r=50, t=50, b=50))
    st.plotly_chart(fig2, use_container_width=True)
    with st.expander("📘 Comment lire cette matrice ?"):
        st.markdown("""
        Cette matrice explore les **corrélations entre les variables liées aux matières dangereuses et le risque composite** :  
        - **Wagons de Matières Dangereuses** : nombre total impliqué.  
        - **Endommagés** : ceux ayant subi un dommage.  
        - **Personnes Évacuées** : conséquence directe d’un danger.  
        Regardez les zones foncées pour détecter les corrélations fortes entre ces variables.
        """)


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
    Ce module repose sur le dataset **[Railroad Accident/Incident Data - Kaggle](https://www.kaggle.com/datasets/chrico03/railroad-accident-and-incident-data)** :
    - **Domaine :** Transport ferroviaire américain
    - **Format :** CSV (nettoyé)
    - **Description :** Plus de 60 000 rapports d'incidents (déraillements, collisions, feux, etc.), incluant type d'accident, état, nombre de personnes concernées, durée, dommages, et coordonnées géographiques.
    - **Pourquoi ce choix ?** : Permet de détecter les zones ferroviaires critiques et d'analyser les types d'incidents impactant la chaîne logistique lourde.

    **Périmètre de l'étude :**
    - L'analyse couvre uniquement les **20 dernières années** (2002-2022) sur la base de la colonne `Report Year`
    - Les enregistrements antérieurs (jusqu'à 1975) ont été **exclus** de l'étude

    **Le `Risque_composite`** est un indicateur calculé à partir de :
    - la fréquence de l'incident
    - la gravité de ses conséquences (victimes, dégâts)
    - le niveau d'évacuation ou impact Hazmat

    > Les valeurs sont normalisées pour aboutir à un `Niveau_criticité` qualitatif : Faible / Moyen / Élevé.
    """)

    # Charger les données nettoyées
    df = load_csv("../data/cleaned/railroad_accident_cleaned.csv")

    # Nettoyage des noms de colonnes (strip des espaces invisibles s'il y en a)
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

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Incidents Totaux", f"{total_incidents:,}")
    col2.metric("Personnes Tuées", f"{total_killed:,}")
    col3.metric("Personnes Blessées", f"{total_injured:,}")
    col4.metric("État + Touché ($)", max_damage_state)

    col1.metric("Dommages Totaux", f"${total_damage:,.0f}")
    col2.metric("Dommage Moyen", f"${avg_damage:,.0f}")
    col3.metric("Plage Temporelle", f"{df["Report Year"].min().astype(int)} - {df["Report Year"].max().astype(int)}")

    tab1, tab2, tab3 = st.tabs(["Vue Globale", "Analyses Temporelle", "Heatmap"])

    with tab1:
        show_tab1(df)

    with tab2:
        show_tab2(df)

    with tab3:
        show_tab3(df)

    st.markdown("---")

    # Résumé
    st.info(f"""
    **Résumé Général des Incidents Ferroviaires :**

    - **Nombre total d'incidents :** {total_incidents:,}
    - **Total de personnes tuées :** {total_killed:,}
    - **Total de personnes blessées :** {total_injured:,}
    - **Coût total des dommages :** ${total_damage:,.0f}
    - **État le plus touché :** {top_state}
    -> Dommages cumulés : ${df[df['State Name'] == top_state]['Total Damage Cost'].sum():,.0f}
    - **Coût moyen par incident :** ${avg_damage:,.0f}
    - **Année la plus critique :** {df['Report Year'].mode()[0]}
    -> Nombre d'incidents : {df['Report Year'].value_counts().max()}
    - **Risque composite moyen :** {df['Risque_composite'].mean():.2e}
    -> (Score faible car basé sur 210M trajets)
    - **Niveau de criticité dominant :** {df['Niveau_criticité'].mode()[0]}
    """)

show()
