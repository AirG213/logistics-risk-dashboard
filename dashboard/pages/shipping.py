import streamlit as st
import base64
from utils import load_csv, apply_responsive
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from sidebar import show_sidebar

show_sidebar()

def show_tab1(df):
    st.markdown("## Répartition des Accidents et du Risque")

    # Gauche : Type d'accident | Droite : Zone géographique
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Par Type d'Accident")
        type_counts = df["Acc_Type"].value_counts().reset_index()
        type_counts.columns = ["Type d'accident", "Nombre"]
        fig_type = px.bar(
            type_counts,
            x="Type d'accident",
            y="Nombre",
            color="Type d'accident",
            title="Nombre d'accidents par type",
            color_discrete_sequence=px.colors.qualitative.Set3,
            text="Nombre"
        )
        fig_type.update_layout(xaxis_tickangle=45, showlegend=False)
        st.plotly_chart(fig_type, use_container_width=True)

    with col2:
        st.subheader("Par Zone Géographique")
        zone_counts = df["Location"].value_counts().reset_index()
        zone_counts.columns = ["Zone", "Nombre"]
        fig_zone = px.pie(
            zone_counts,
            names="Zone",
            values="Nombre",
            title="Répartition géographique des accidents",
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        st.plotly_chart(apply_responsive(fig_zone), use_container_width=True)

    with st.expander("📊 Interprétation des graphiques"):
        st.markdown("""
        - **Type d'accident** : La plupart des incidents sont dus à des **erreurs de navigation ou de manoeuvre** (telles que des collisions, des échouements...), qui représentent environ 58 % des cas. Ils sont suivis par des accidents non classés (catégorie "Autre"), qui comptent pour 27 %. Les autres types d'incidents demeurent marginaux.
        - **Zone géographique** : Les accidents surviennent principalement en **mer côtière** (43%), puis **en approche du port** (26%) et en **zone portuaire** (18%). La **mer ouverte** est la zone la moins touchée (12%).
        """)

    st.markdown("""> **Note :** Les zones géographiques sont définies comme suit :
> - **Port** : Zone portuaire (zone de 3 km autour du port)
> - **Approche portuaire** : Zone de 10 km autour du port
> - **Mer côtière** : Zone maritime au-delà de 10 km du port
> - **Mer ouverte** : Au-delà de 22 km du littoral (hors des eaux territoriales)
    """)

    st.markdown("---")

    # Gauche : Classe de Risque | Droite : Distribution Risk Score
    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Par Classe de Risque")
        risk_counts = df["Risk_Class"].value_counts().reset_index()
        risk_counts.columns = ["Classe de Risque", "Nombre"]
        fig_risk = px.pie(
            risk_counts,
            names="Classe de Risque",
            values="Nombre",
            title="Niveau de Risque des Accidents",
            color="Classe de Risque",
            color_discrete_map={
                "Bas": "#2ecc71",
                "Medium": "#f1c40f",
                "Haut": "#e67e22",
                "Critique": "#e74c3c",
            },
            category_orders={"Classe de Risque": ["Bas", "Medium", "Haut", "Critique"]},
        )
        st.plotly_chart(apply_responsive(fig_risk), use_container_width=True)

    q = df['Risk_Score'].quantile([0, 0.25, 0.5, 0.75, 1]).values

    with col4:
        st.subheader("Distribution du Score de Risque")
        fig_dist = px.histogram(
            df,
            x="Risk_Score",
            nbins=80,
            title="Distribution des Scores de Risque",
            labels={"Risk_Score": "Score de Risque"},
            color_discrete_sequence=["#3498db"],
            opacity=0.85,
            log_y=True
        )
        fig_dist.update_layout(
            xaxis_title="Score de Risque",
            yaxis_title="Nombre d'accidents (échelle log)",
            bargap=0.05
        )
        st.plotly_chart(fig_dist, use_container_width=True)

    with st.expander("💡 Interprétation des Scores de Risque"):
        st.markdown(f"""
        Le **Score de Risque** est un indicateur composite calculé à partir d'une pondération des dommages matériels, de la pollution et du profil du navire.

        **Seuils de classification utilisés (dynamiquement par quantiles) :**
        - **Bas** : 0 ≤ score ≤ `{q[1]:.3f}`
        - **Medium** : `{q[1]:.3f}` < score ≤ `{q[2]:.3f}`
        - **Haut** : `{q[2]:.3f}` < score ≤ `{q[3]:.3f}`
        - **Critique** : `{q[3]:.3f}` < score ≤ `{q[4]:.3f}`

        > Ces seuils permettent de diviser les incidents en **quatre groupes de gravité**, selon la distribution des risques dans le dataset.
        """)


def show_tab2(df):
    st.markdown("## Analyse Temporelle et Cartographie")

    # Conversion explicite des années en entiers pour animation
    df["Year"] = df["Year"].astype("Int64")

    # Carte des incidents animée par année
    st.subheader("Cartographie Animée des Accidents Maritimes")
    fig_map = px.density_map(
        df,
        lat="Latitude",
        lon="Longitude",
        z=[1]*len(df),
        radius=5,
        hover_name="Acc_Type",
        hover_data=["Risk_Score", "Location"],
        color_continuous_scale='viridis',
        zoom=3,
        height=500,
        animation_frame="Year",
        animation_group="Unique_ID",
        labels={"z": "Densité", "Year": "Année", "Unique_ID": "ID Unique", "Risk_Score": "Score de Risque", "Location": "Zone Géographique"},
    )
    fig_map.update_layout(mapbox_style="carto-positron", margin={"r":0,"t":0,"l":0,"b":0})
    fig_map.update_layout(transition_duration=500)
    fig_map.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))
    st.plotly_chart(apply_responsive(fig_map), use_container_width=True)

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Évolution du Nombre d'Accidents par Année")
        yearly_counts = df["Year"].value_counts().sort_index()
        fig_years = px.line(
            x=yearly_counts.index,
            y=yearly_counts.values,
            labels={"x": "Année", "y": "Nombre d'accidents"},
            markers=True
        )
        fig_years.update_layout(title="Accidents par an")
        st.plotly_chart(fig_years, use_container_width=True)

        with st.expander("📊 Interprétation du graphique"):
            st.markdown("""
            - **2003-2017** : Période de faible activité, avec un nombre d'accidents entre 50 et 200 par an.
            - **2018-2023** : Forte augmentation, culminant à plus de 438 incidents en 2021.
            """)

    with col2:
        st.subheader("Évolution du Score de Risque Moyen par Année")
        df_yearly_risk = df.groupby("Year")["Risk_Score"].mean().reset_index()
        fig_risk = px.line(
            df_yearly_risk,
            x="Year",
            y="Risk_Score",
            labels={"Risk_Score": "Score de Risque Moyen", "Year": "Année"},
            markers=True
        )
        fig_risk.update_layout(title="Score de Risque Moyen par Année", yaxis_range=[0, 0.1])
        st.plotly_chart(fig_risk, use_container_width=True)

        with st.expander("📊 Interprétation du graphique"):
            st.markdown("""
            Malgré des piques de risque en 2003, 2006, 2010 et 2015, le score moyen reste relativement stable autour de 0.015 - 0.020
            """)

def show_tab3(df):
    st.markdown("## Corrélations entre Zones, Types et Risques")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Type d'accident vs Zone géographique")
        heatmap1 = pd.crosstab(df['Acc_Type'], df['Geo_Zone'])
        fig1 = px.imshow(
            heatmap1,
            labels=dict(x="Zone", y="Type", color="Nombre"),
            color_continuous_scale="Blues",
            text_auto=True,
            aspect="auto"
        )
        fig1.update_layout(margin=dict(t=40, l=0, r=0, b=0))
        st.plotly_chart(apply_responsive(fig1), use_container_width=True)

    with col2:
        st.subheader("Zone géographique vs Classe de Risque")
        heatmap2 = pd.crosstab(df['Geo_Zone'], df['Risk_Class'])
        fig2 = px.imshow(
            heatmap2,
            labels=dict(x="Classe de Risque", y="Zone", color="Nombre"),
            color_continuous_scale="Reds",
            text_auto=True,
            aspect="auto"
        )
        fig2.update_layout(margin=dict(t=40, l=0, r=0, b=0))
        st.plotly_chart(apply_responsive(fig2), use_container_width=True)

    st.markdown("---")

    # Deuxième ligne : Type d'accident vs Classe de risque
    st.subheader("Type d'accident vs Classe de Risque")
    heatmap3 = pd.crosstab(df['Acc_Type'], df['Risk_Class'])
    fig3 = px.imshow(
        heatmap3,
        labels=dict(x="Classe de Risque", y="Type d'accident", color="Nombre"),
        color_continuous_scale="Purples",
        text_auto=True,
        aspect="auto"
    )
    fig3.update_layout(margin=dict(t=40, l=0, r=0, b=0))
    st.plotly_chart(apply_responsive(fig3), use_container_width=True)

    with st.expander("📊 Interprétation des graphiques"):
        st.markdown("""
        La majorité des accidents sont des **erreurs de navigation ou de manoeuvre**, survenant principalement dans le **Nord-Est** et le **Sud** / **Sud-Ouest** de la mer Baltique. La gravité des incidents est généralement **Critique** dans ces zones.
        """)

    st.markdown("---")

    st.subheader("Risque Moyen par Zone")
    df["Zone_Geo"] = df["Geo_Latitude_Zone"] + " / " + df["Geo_Longitude_Zone"]
    heatmap_data = df.groupby("Zone_Geo")["Risk_Score"].mean().reset_index()
    heatmap_data["Latitude"] = heatmap_data["Zone_Geo"].apply(lambda x: x.split(" / ")[0])
    heatmap_data["Longitude"] = heatmap_data["Zone_Geo"].apply(lambda x: x.split(" / ")[1])

    fig3 = px.density_heatmap(
        heatmap_data,
        x="Longitude",
        y="Latitude",
        z="Risk_Score",
        color_continuous_scale="YlOrRd",
        labels={"Risk_Score": "Score de Risque Moyen"},
    )
    fig3.update_layout(
        xaxis_title="Zone Longitudinale",
        yaxis_title="Zone Latitudinale",
        margin=dict(t=30, l=0, r=0, b=0)
    )
    st.plotly_chart(apply_responsive(fig3), use_container_width=True)

def show():
    # Charger l'icône et encoder en base64
    with open("assets/shipping_icon.png", "rb") as f:
        icon_base64 = base64.b64encode(f.read()).decode()

    # Titre + Icône alignés
    st.markdown(
        f"""
        <div style="display: flex; align-items: center;">
            <img src="data:image/png;base64,{icon_base64}" alt="Icone" style="width:60px; margin-right: 10px;">
            <h1 style="margin: 0;">Analyse de Risque — Accidents Maritimes (Baltique)</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("""
    ### Contexte et Sources des Données

    Ce module repose sur une analyse approfondie des **accidents maritimes survenus en mer Baltique** entre 2003 et 2023. Il s'appuie sur plusieurs jeux de données géospatiaux fiables permettant une **cartographie précise** et une **classification des risques logistiques maritimes**.

    #### Données utilisées :
    - **[HELCOM - Baltic Sea Shipping Accidents Database](https://maps.helcom.fi/website/mapservice/?datasetID=cae61cf8-0b3a-449a-aeaf-1df752dd3d80)**
      > Base officielle recensant chaque accident en mer ou en zone portuaire : localisation, type, cause, navire impliqué, pollution, dommages, etc.

    - **[World Port Index](https://fgmod.nga.mil/apps/WPI-Viewer/)**
      > Référentiel mondial des ports (coordonnées, infrastructures, capacité).

    - **[Natural Earth](https://www.naturalearthdata.com/downloads/10m-physical-vectors/10m-land/)**
      > Cartographie des côtes pour identifier les zones proches du littoral.

    #### Méthodologie :
    - **Regroupement des accidents en 5 catégories :**
      `Technical or Equipment Failure`, `Navigation or Maneuvering Incident`, `Fire or Explosion`, `Life-saving Equipment Incident`, `Other`

    - **Classification géographique des lieux d'accident :**
      `Port`, `Port approach`, `Sea`, `Open sea`
      → basée sur des calculs de distance entre les accidents, les côtes et les ports.

    - **Calcul du Score de Risque :**
      Chaque incident est évalué à travers un score composite calculé comme une moyenne pondérée de trois dimensions : la sévérité des dommages, le niveau de pollution, et le profil de vulnérabilité du navire. Ce score, compris entre 0 et 1, est défini par la formule suivante :
      `Risk_Score = 0.5 x Damage_Severe + 0.3 x Pollution_Score + 0.2 x Ship_Profile_Score`
    """)

    # Charger les données nettoyées
    df = load_csv("../data/cleaned/shipping_accidents_cleaned.csv")

    # Aperçu dans un expander
    with st.expander("Voir un aperçu du dataset (1000 lignes)"):
        st.dataframe(df.head(1000))

    # KPI globaux
    st.markdown("### Indicateurs Clés Globaux")

    total_accidents = df.shape[0]
    most_common_type = df["Acc_Type"].mode()[0]
    year_min = int(df["Year"].min())
    year_max = int(df["Year"].max())
    distinct_years = df["Year"].nunique()
    most_common_zone = df["Location"].mode()[0]

    # Calcul pollution totale si la colonne existe
    if "Pollution_Score" in df.columns:
        pollution_sum = df["Pollution_Score"].fillna(0).sum()
        pollution_display = f"{pollution_sum:,.2f} tonnes" if pollution_sum > 0 else "Donnée indisponible"
    else:
        pollution_display = "Donnée indisponible"

    col1, col2, col3 = st.columns(3)
    col1.metric("Nombre total d'accidents", f"{total_accidents:,}")
    col2.metric("Type d'accident le plus fréquent", most_common_type)
    col3.metric("Plage temporelle", f"{year_min} - {year_max}")

    col1.metric("Zone géographique la plus touchée", most_common_zone)
    col2.metric("Pollution totale (tonnes)", pollution_display)

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
    **Résumé du module :**
    - Accidents les plus fréquents : **{most_common_type}**, représentant {df['Acc_Type'].value_counts(normalize=True).max()*100:.1f}% des cas.
    - Zone la plus touchée : **{most_common_zone}** ({df['Location'].value_counts(normalize=True).max()*100:.1f}% des incidents).
    - Score de risque moyen : **{df['Risk_Score'].mean():.3f}** (min: {df['Risk_Score'].min():.3f}, max: {df['Risk_Score'].max():.3f}).
    - Pollution totale estimée : **{pollution_display}**.
    - Plage d'analyse : **{year_min} → {year_max}**, couvrant {distinct_years} années.
    - Incidents critiques (classe "Critique") : **{(df['Risk_Class'] == 'Critique').mean()*100:.1f}%** du total.
    """)

show()
