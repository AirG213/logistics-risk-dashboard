import streamlit as st
import plotly.express as px
import pandas as pd
from utils import load_csv, apply_responsive, get_base64
from sidebar import show_sidebar

show_sidebar()

icon_base64 = get_base64('assets/traffic_accident_icon.png')

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

    st.markdown("""
    ### Contexte et Source des Données

    Ce module est basé sur le dataset **[US Accidents (2016-2023)](https://www.kaggle.com/datasets/sobhanmoosavi/us-accidents)** :
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

    # Charger les données
    df = load_csv("../data/cleaned/usa_accidents_traffic_cleaned.csv")
    df['Start_Time'] = pd.to_datetime(df['Start_Time']) # dates sont au format datetime

    # Aperçu du CSV
    with st.expander("Voir un aperçu du dataset (1000 lignes)"):
        st.dataframe(df.head(1000))

    # Préparer les agrégats
    hour_counts, day_counts, month_counts, hour_scores, day_scores, month_scores, risk_summary, heatmap = prepare_data(df)

    # KPI
    total = df.shape[0]
    peak_hour_pct = (df[df['Risk_Category'] == 'Heure de Pointe'].shape[0] / total) * 100
    infra_block_mean = df[df['Risk_Category'] == 'Blocage Infrastructure']['Duration(min)'].mean()
    weather_pct = (df[df['Risk_Category'] == 'Perturbation Météo'].shape[0] / total) * 100
    df['Start_Time'] = pd.to_datetime(df['Start_Time'])

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric('Heures de pointe', f'{peak_hour_pct:.1f} %')
    col2.metric('Durée Blocage Moyenne', f'{infra_block_mean:.0f} min')
    col3.metric('Perturbations Météo', f'{weather_pct:.1f} %')
    col4.metric('Total Accidents', f'{total:,}')
    col5.metric('Plage Temporelle', f'{df['Start_Time'].min().year} - {df['Start_Time'].max().year}')

    # TABS pour structurer la page
    tab1, tab2, tab3 = st.tabs(['Vue Globale', 'Analyses Temporelle', 'Matrice de Corrélation'])

    with tab1:
        st.subheader('Répartition des Catégories de Risque')
        fig_cat = px.bar(
            risk_summary,
            x='Count',
            y='Risk_Category',
            orientation='h',
            text='Proportion (%)',
            color='Risk_Category',
            color_discrete_sequence=px.colors.qualitative.Set2,
            labels={
                'Count': "Nombre d'incidents",
                'Risk_Category': "Catégorie de Risque"
            }
        )
        st.plotly_chart(apply_responsive(fig_cat), use_container_width=True)

        with st.expander("📊 Interprétation du graphique"):
            st.markdown("""
            Ce graphique illustre la **répartition des incidents** selon différentes catégories de risque.  
            - L'axe horizontal représente le **nombre total d'incidents** enregistrés.
            - L'axe vertical indique la **catégorie de risque**.
            Cela permet de visualiser rapidement les types de risques les plus fréquents.
            """)
        st.markdown('---')

    with tab2:
        st.subheader('Analyse par Heure de la Journée')

        fig_hour_count = px.bar(
            hour_counts, x='HourOfDay', y='Count',
            labels={'HourOfDay': 'Heure', 'Count': "Nombre d'incidents"}
        )
        st.plotly_chart(apply_responsive(fig_hour_count), use_container_width=True)
        with st.expander("📊 Comment lire ce graphique ?"):
            st.markdown("Ce graphique montre le **nombre total d’incidents** selon l’heure de la journée (0 = minuit, 23 = 23h).")

        fig_hour_score = px.line(
            hour_scores, x='HourOfDay', y='Risk_Score', markers=True,
            labels={'HourOfDay': 'Heure', 'Risk_Score': "Score de Risque"}
        )
        st.plotly_chart(apply_responsive(fig_hour_score), use_container_width=True)
        with st.expander("📊 Comment lire ce graphique ?"):
            st.markdown("Ce graphique montre l’**évolution du score de risque moyen** en fonction de l’heure de l’incident.")

        st.markdown('---')

        st.subheader('Analyse par Jour de la Semaine')

        fig_day_count = px.bar(
            day_counts, x='DayOfWeek', y='Count',
            labels={'DayOfWeek': 'Jour de la semaine (0 = Lundi)', 'Count': "Nombre d'incidents"}
        )
        st.plotly_chart(apply_responsive(fig_day_count), use_container_width=True)
        with st.expander("📊 Comment lire ce graphique ?"):
            st.markdown("Ce graphique affiche le **nombre total d’incidents** pour chaque jour de la semaine. (0 = Lundi, 6 = Dimanche)")

        fig_day_score = px.line(
            day_scores, x='DayOfWeek', y='Risk_Score', markers=True,
            labels={'DayOfWeek': 'Jour de la semaine (0 = Lundi)', 'Risk_Score': "Score de Risque"}
        )
        st.plotly_chart(apply_responsive(fig_day_score), use_container_width=True)
        with st.expander("📊 Comment lire ce graphique ?"):
            st.markdown("Ce graphique montre le **score de risque moyen** associé à chaque jour de la semaine.")

        st.markdown('---')

        st.subheader('Analyse par Mois')

        fig_month_count = px.bar(
            month_counts, x='Month', y='Count',
            labels={'Month': 'Mois', 'Count': "Nombre d'incidents"}
        )
        st.plotly_chart(apply_responsive(fig_month_count), use_container_width=True)
        with st.expander("📊 Comment lire ce graphique ?"):
            st.markdown("Ce graphique indique le **volume d’incidents** par mois sur la période analysée.")

        fig_month_score = px.line(
            month_scores, x='Month', y='Risk_Score', markers=True,
            labels={'Month': 'Mois', 'Risk_Score': "Score de Risque"}
        )
        st.plotly_chart(apply_responsive(fig_month_score), use_container_width=True)
        with st.expander("📊 Comment lire ce graphique ?"):
            st.markdown("Ce graphique montre **l’évolution du score de risque moyen par mois**.")


    with tab3:
    
        st.subheader("Heatmap Risk_Score (Météo vs Heure)")
        df['HourGroupStart'] = (df['HourOfDay'] // 2) * 2
        df['HourGroup'] = df['HourGroupStart'].astype(str) + "h-" + (df['HourGroupStart'] + 2).astype(str) + "h"
        hour_order = [f"{h}h-{h+2}h" for h in range(0, 24, 2)]
        df['HourGroup'] = pd.Categorical(df['HourGroup'], categories=hour_order, ordered=True)
        weather_order = ['Clair', 'Brouillard', 'Pluie', 'Neige', 'Orage', 'Autres']
        df['Main_Weather'] = df['Main_Weather'].astype(str).str.strip()
        df['Main_Weather'] = df['Main_Weather'].replace("", "Autres")
        df['Main_Weather'] = df['Main_Weather'].where(df['Main_Weather'].isin(weather_order), "Autres")
        df['Main_Weather'] = pd.Categorical(df['Main_Weather'], categories=weather_order, ordered=True)
        heatmap_pivot = df.pivot_table(
            index="Main_Weather",
            columns="HourGroup",
            values="Risk_Score",
            aggfunc="mean",
            observed=False
        ).round(2)
        fig = px.imshow(
            heatmap_pivot.values,
            labels={"x": "Heure de la Journée", "y": "Conditions Météo", "color": "Score de Risque"},
            x=heatmap_pivot.columns,
            y=heatmap_pivot.index,
            color_continuous_scale="Reds",
            text_auto=".2f",
            title="Carte de Chaleur du Risque (Météo vs Heure)"
        )
        st.plotly_chart(apply_responsive(fig), use_container_width=True)
        with st.expander("🧠 Comment lire cette heatmap ?"):
            st.markdown("""
            Cette carte montre la **moyenne des scores de risque** en fonction de l'**heure de la journée** (par tranches de 2h)  
            et des **conditions météorologiques**.

            - Les **zones plus sombres** indiquent un **risque plus élevé**.
            - Cela permet d'identifier les créneaux horaires et conditions météo les plus critiques.
            """)
        st.markdown('---')

        # Météo x Jour de la Semaine
        st.subheader("Carte de Chaleur du Risque (Météo vs Jour de la Semaine)")
        # Traduction des jours
        jours_fr = {
            0: "Lundi", 1: "Mardi", 2: "Mercredi", 3: "Jeudi",
            4: "Vendredi", 5: "Samedi", 6: "Dimanche"
        }
        df["DayOfWeek_fr"] = df["DayOfWeek"].map(jours_fr)
        # Matrice de corrélation
        heatmap_week = df.pivot_table(
            index="Main_Weather",
            columns="DayOfWeek_fr",
            values="Risk_Score",
            aggfunc="mean",
            observed=False
        ).round(2)
        # Reordonne les jours
        heatmap_week = heatmap_week[["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]]
        # Affichage
        fig_week = px.imshow(
            heatmap_week,
            labels=dict(x="Jour de la Semaine", y="Conditions Météo", color="Score de Risque"),
            color_continuous_scale="Reds",
            text_auto=True,
            aspect="auto",
            title="Score de Risque Moyen selon la Météo et le Jour"
        )
        st.plotly_chart(apply_responsive(fig_week), use_container_width=True)
        with st.expander("📌 Comment lire cette heatmap ?"):
            st.markdown("""
            Cette carte montre la moyenne des **scores de risque** en fonction des **conditions météo** (axe Y) et du **jour de la semaine** (axe X).

            Elle permet d’identifier les jours où les conditions météo influencent le plus les risques, comme le lundi pluvieux ou le samedi enneigé.
            """)
        st.markdown("---")

    # Résumé
    st.info(f"""
    **Résumé du module :**
    - Heures de pointe : {peak_hour_pct:.1f}% des incidents contribuent directement à la congestion.
    - Incidents « Blocage Infrastructure » : durée moyenne {infra_block_mean:.0f} minutes.
    - Perturbations météo : {weather_pct:.1f}% des cas (pluie, neige, brouillard).
    - Total incidents analysés : {total:,}.
    """)

show()
