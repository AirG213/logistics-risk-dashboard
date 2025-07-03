import streamlit as st
import pandas as pd
import base64
from utils import load_csv, apply_responsive
import plotly.express as px
from sidebar import show_sidebar

show_sidebar()

def show_tab1(df):
    # 1. Histogramme - Temps de Livraison
    st.markdown("### Répartition des Temps de Livraison (en minutes)")
    fig_hist = px.histogram(
        df,
        x="Delivery_Time",
        nbins=50,
        labels={"Delivery_Time": "Temps de Livraison (minutes)"},
        color_discrete_sequence=["#1f77b4"]
    )
    fig_hist.update_yaxes(title_text="Nombre de commandes")
    st.plotly_chart(apply_responsive(fig_hist), use_container_width=True)

    with st.expander("📊 Interprétation du graphique"):
        st.markdown("""
        Ce graphique montre la **distribution des temps de livraison** pour les commandes Amazon simulées.  
        Chaque barre représente le **nombre de livraisons** réalisées dans une plage de temps donnée (en minutes).

        - Une **concentration élevée à gauche** signifie que la majorité des livraisons sont rapides.
        - Une **queue étendue à droite** peut indiquer des retards ou des zones problématiques.
        """)

    st.markdown("---")

    # 2. Contextes à Risque (Météo x Circulation)
    st.markdown("### Contextes les Plus à Risque (Météo & Circulation)")
    top_risks = (
        df.groupby(['Weather', 'Traffic'])['delivery_risk']
        .mean()
        .sort_values(ascending=False)
        .head(5)
        .reset_index()
    )
    st.dataframe(top_risks.rename(columns={
        "Weather": "Conditions Météo",
        "Traffic": "Conditions de Circulation",
        "delivery_risk": "Score de Risque Moyen"
    }), hide_index=True, use_container_width=True)

    with st.expander("📊 Interprétation du tableau"):
        st.markdown("""
        Ce tableau affiche les combinaisons météo + trafic qui présentent le **plus haut risque moyen de retard**.
        Cela permet d’identifier les situations critiques à anticiper.
        """)

    st.markdown("---")

    # 3. Zones Géographiques à Risque
    st.markdown("### Zones Géographiques à Risque")

    df['Area_cleaned'] = df['Area'].str.strip()

    area_risks = (
        df.groupby('Area_cleaned', as_index=False)['area_risk_score']
        .mean()
        .sort_values(by="area_risk_score", ascending=False)
    )

    st.dataframe(area_risks.rename(columns={
        "Area_cleaned": "Zone",
        "area_risk_score": "Score de Risque Moyen"
    }), hide_index=True, use_container_width=True)

    with st.expander("📊 Interprétation du tableau"):
        st.markdown("""
        Ce tableau montre quelles zones géographiques (urbaines, semi-urbaines, etc.) sont les plus sujettes aux retards de livraison.
        """)

    st.markdown("---")

    # 4. Catégories les plus Commandées
    st.markdown("### Catégories de Produits les plus Commandées")
    top_categories = (
        df['Category'].value_counts()
        .reset_index()
        .rename(columns={'index': 'Catégorie', 'Category': 'Occurrences'})
    ).head(5)
    st.dataframe(top_categories, hide_index=True, use_container_width=True)

    with st.expander("📊 Interprétation du tableau"):
        st.markdown("""
        Ce tableau met en avant les **catégories de produits** les plus souvent commandées. Cela peut indiquer les préférences des clients.
        """)

def show_tab2(df):
    df_time = df.copy()
    df_time["Order_Date"] = pd.to_datetime(df_time["Order_Date"], errors="coerce")
    df_time["Order_Hour"] = pd.to_datetime(df_time["Order_Time"], format="%H:%M:%S", errors="coerce").dt.hour
    df_time["Pickup_Hour"] = pd.to_datetime(df_time["Pickup_Time"], format="%H:%M:%S", errors="coerce").dt.hour
    df_time["DayOfWeek"] = df_time["Order_Date"].dt.day_name()

    # Bloc 1
    st.subheader("Volume de Commandes par Heure de la Journée")
    fig_orders = px.histogram(df_time, x="Order_Hour", nbins=24,
                            labels={
                                "Order_Hour": "Heure",
                                "y": "Nombre de commandes"
                            },                              
                            title="Nombre de commandes passées par heure",
                            color_discrete_sequence=["#006eff"])
    fig_orders.update_layout(margin=dict(l=0, r=0, t=40, b=0))
    fig_orders.update_yaxes(title_text="Nombre de commandes")
    st.plotly_chart(apply_responsive(fig_orders), use_container_width=True)
    with st.expander("🧠 Comment lire ce graphique ?"):
        st.write("Ce graphique montre à quelles heures les clients passent le plus de commandes. Cela peut refléter les pics d'activité journaliers.")

    st.markdown("---")

    # Bloc 2
    st.subheader("Temps de Livraison selon l'Heure de Commande")
    fig_box = px.box(df_time, x="Order_Hour", y="Delivery_Time",
                     labels={"Order_Hour": "Heure", "Delivery_Time": "Temps de livraison (min)"},
                     title="Distribution des délais selon l'heure de la commande",
                     color_discrete_sequence=["#9b59b6"])
    st.plotly_chart(apply_responsive(fig_box), use_container_width=True)
    with st.expander("🧠 Comment lire ce graphique ?"):
        st.write("Ce graphique montre la distribution des durées de livraison selon l'heure à laquelle la commande est passée. Il permet d'observer les heures à risques.")

    st.markdown("---")

    # Bloc 3
    st.subheader("Taux de Retard (>120min) par Heure")
    risk_by_hour = df_time.groupby("Order_Hour")["delivery_risk"].mean().reset_index()
    fig_risk_hour = px.line(risk_by_hour, x="Order_Hour", y="delivery_risk", markers=True,
                            labels={"Order_Hour": "Heure de commande", "delivery_risk": "Taux de retard"},
                            title="Proportion de retards selon l'heure de la commande",
                            color_discrete_sequence=["#e74c3c"])
    fig_risk_hour.update_layout(yaxis_tickformat=".0%", margin=dict(l=0, r=0, t=40, b=0))
    st.plotly_chart(apply_responsive(fig_risk_hour), use_container_width=True)
    with st.expander("🧠 Comment lire ce graphique ?"):
        st.write("Ce graphique indique la proportion moyenne de livraisons retardées en fonction de l’heure de commande.")

    st.markdown("---")

    # Bloc 4
    st.subheader("Taux de Retard selon le Jour de la Semaine")
    # --- Ajout du mapping FR ---
    mapping_weekday = {
        "Monday": "Lundi",
        "Tuesday": "Mardi",
        "Wednesday": "Mercredi",
        "Thursday": "Jeudi",
        "Friday": "Vendredi",
        "Saturday": "Samedi",
        "Sunday": "Dimanche"
    }
    ordered_days_fr = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
    df_time["DayOfWeek_FR"] = df_time["DayOfWeek"].replace(mapping_weekday)
    risk_by_day = df_time.groupby("DayOfWeek_FR")["delivery_risk"].mean().reindex(ordered_days_fr).reset_index()
    fig_risk_day = px.bar(
        risk_by_day, x="DayOfWeek_FR", y="delivery_risk",
        labels={"DayOfWeek_FR": "Jour de la semaine", "delivery_risk": "Taux de retard"},
        title="Retards moyens par jour de la semaine",
        color_discrete_sequence=["#f39c12"]
    )
    fig_risk_day.update_layout(yaxis_tickformat=".0%", margin=dict(l=0, r=0, t=40, b=0))
    st.plotly_chart(apply_responsive(fig_risk_day), use_container_width=True)
    with st.expander("🧠 Comment lire ce graphique ?"):
        st.write("Ce graphique montre quel jour de la semaine connaît en moyenne le plus de retards dans les livraisons.")

    st.markdown("---")

    # Bloc 5
    st.subheader("Matin vs Soir : Comparaison du Taux de Retard")
    df_time["Period"] = df_time["Order_Hour"].apply(lambda h: "Matin (6h-12h)" if 6 <= h < 12 else
                                                               "Après-midi (12h-18h)" if 12 <= h < 18 else
                                                               "Soir/Nuit (18h-6h)")
    risk_by_period = df_time.groupby("Period")["delivery_risk"].mean().reindex([
        "Matin (6h-12h)", "Après-midi (12h-18h)", "Soir/Nuit (18h-6h)"]).reset_index()
    fig_risk_period = px.bar(risk_by_period, x="Period", y="delivery_risk",
                             labels={"Period": "Période", "delivery_risk": "Taux de retard"},
                             title="Taux de retard en fonction du moment de la journée",
                             color_discrete_sequence=["#1abc9c"])
    fig_risk_period.update_layout(yaxis_tickformat=".0%", margin=dict(l=0, r=0, t=40, b=0))
    st.plotly_chart(apply_responsive(fig_risk_period), use_container_width=True)
    with st.expander("🧠 Comment lire ce graphique ?"):
        st.write("Cette comparaison permet de voir à quels moments de la journée les risques de retard sont les plus élevés.")

    st.markdown("---")

    # Bloc 6
    st.subheader("Évolution Globale du Taux de Retard")
    risk_by_date = df_time.groupby("Order_Date")["delivery_risk"].mean().reset_index()
    fig_date = px.line(risk_by_date, x="Order_Date", y="delivery_risk", markers=True,
                       labels={"Order_Date": "Date de commande", "delivery_risk": "Taux de retard"},
                       title="Évolution du risque de retard sur la période analysée",
                       color_discrete_sequence=["#2980b9"])
    fig_date.update_layout(yaxis_tickformat=".0%", margin=dict(l=0, r=0, t=40, b=0))
    st.plotly_chart(apply_responsive(fig_date), use_container_width=True)
    with st.expander("🧠 Comment lire ce graphique ?"):
        st.write("Ce graphique montre la tendance générale des retards dans le temps, ce qui peut révéler une amélioration ou une détérioration du service.")

def show_tab3(df):
    # Bloc 1 — Météo × Trafic
    st.subheader("Carte des Risques — Météo x Trafic")
    risk_weather_traffic = df.pivot_table(index="Weather", columns="Traffic", values="delivery_risk", aggfunc="mean")
    fig1 = px.imshow(
        risk_weather_traffic,
        text_auto=".2f",
        color_continuous_scale="Reds",
        aspect="auto",
        labels=dict(x="Trafic", y="Météo", color="Taux de retard"),
        title="Taux de retard (>120min) selon Météo et Trafic"
    )
    st.plotly_chart(apply_responsive(fig1), use_container_width=True)
    with st.expander("🧠 Interprétation de la carte Météo x Trafic"):
        st.markdown("""
        Cette carte montre le **taux moyen de retard** en fonction des conditions météorologiques et de circulation.  
        Les cellules les plus rouges signalent les **contextes les plus critiques** (ex : orage + embouteillage).
        """)

    st.markdown("---")

    # Bloc 2 — Zone x Météo
    st.subheader("Carte des Risques — Zone x Météo")
    risk_area_weather = df.pivot_table(index="Weather", columns="Area", values="delivery_risk", aggfunc="mean")
    fig2 = px.imshow(
        risk_area_weather,
        text_auto=".2f",
        color_continuous_scale="Oranges",
        aspect="auto",
        labels=dict(x="Zone", y="Météo", color="Taux de retard"),
        title="Taux de retard selon Zone et Météo"
    )
    st.plotly_chart(apply_responsive(fig2), use_container_width=True)
    with st.expander("🧠 Interprétation de la carte Zone x Météo"):
        st.markdown("""
        Cette carte croise les zones géographiques avec les conditions météo pour révéler les **zones les plus sensibles** aux retards.
        """)

    st.markdown("---")

    # Bloc 3 — Jour x Heure
    st.subheader("Carte des Risques — Jour x Heure de Commande")
    df["Order_Hour"] = pd.to_datetime(df["Order_Time"], format="%H:%M:%S", errors="coerce").dt.hour
    df["DayOfWeek"] = pd.to_datetime(df["Order_Date"], format="%Y-%m-%d", errors="coerce").dt.day_name()
    mapping_weekday = {
        "Monday": "Lundi",
        "Tuesday": "Mardi",
        "Wednesday": "Mercredi",
        "Thursday": "Jeudi",
        "Friday": "Vendredi",
        "Saturday": "Samedi",
        "Sunday": "Dimanche"
    }
    ordered_days_fr = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
    df["DayOfWeek_FR"] = df["DayOfWeek"].replace(mapping_weekday)
    risk_day_hour = df.pivot_table(
        index="DayOfWeek_FR",
        columns="Order_Hour",
        values="delivery_risk",
        aggfunc="mean"
    )
    risk_day_hour = risk_day_hour.reindex(ordered_days_fr)
    fig3 = px.imshow(
        risk_day_hour,
        text_auto=False,
        color_continuous_scale="Purples",
        aspect="auto",
        labels=dict(x="Heure de commande", y="Jour de la semaine", color="Taux de retard"),
        title="Retards selon le Jour et l'Heure de Commande"
    )
    st.plotly_chart(apply_responsive(fig3), use_container_width=True)
    with st.expander("🧠 Interprétation de la carte Jour x Heure"):
        st.markdown("""
        Cette carte permet d’identifier **les moments les plus propices aux retards** selon le jour et l’heure de la commande.  
        Elle est utile pour ajuster les stratégies logistiques en fonction du calendrier.
        """)

def show():
    # Charger l'icône et encoder en base64
    with open("assets/amazon_icon.png", "rb") as f:
        icon_base64 = base64.b64encode(f.read()).decode()

    # Titre + Icône alignés
    st.markdown(
        f"""
        <div style="display: flex; align-items: center;">
            <img src="data:image/png;base64,{icon_base64}" alt="Icone" style="width:60px; margin-right: 10px;">
            <h1 style="margin: 0;">Analyse de Risque — Livraison Amazon (Dernier Kilomètre)</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("""
    ### Contexte et Source des Données

    Ce module repose sur le dataset **[Amazon Delivery Dataset - Sujal Suthar (Kaggle)](https://www.kaggle.com/datasets/sujalsuthar/amazon-delivery-dataset)** :
    - **Domaine :** Transport routier / Logistique du dernier kilomètre
    - **Format :** CSV (~43 000 lignes)
    - **Description :** Données issues de livraisons Amazon en environnement urbain et métropolitain, incluant météo, circulation, zone géographique, performance de livraison, et type de véhicule.
    - **Pourquoi ce choix ?** : Permet d'illustrer l'impact des conditions météo et du trafic sur les retards, d'identifier les situations critiques, et d'évaluer la résilience opérationnelle sur le dernier kilomètre.

    > ℹ️ **Attention :** La provenance exacte du dataset n'est pas garantie. Il est probable qu'il s'agisse de données simulées ou anonymisées à des fins pédagogiques. Les analyses restent néanmoins pertinentes pour étudier les facteurs logistiques impactant la performance de livraison.

    ---

    ### Variables Clés

    - **`delivery_risk`**
    > Définit comme `1` si `Delivery_Time > 120 min`, sinon `0`.
    > Permet d'isoler les livraisons considérées comme en **retard important**.

    - **`weather_traffic_risk_score`**
    > Calculé à partir du **taux moyen de retards** (>120 min) **observé pour chaque combinaison `Weather` x `Traffic`** (via une pivot table).
    > Exemple : `Cloudy + Jam` ≈ 89 % de livraisons en retard → score = 0.89.

    - **`area_risk_score`**
    > Moyenne des `delivery_risk` par type de zone (`Area`) : `Urban`, `Metropolitian`, etc.
    > Exemple : si 37 % des livraisons en zone urbaine sont en retard, score = 0.37.
    Toutes ces variables sont ajoutées dynamiquement dans le jeu de données nettoyé **`amazon_delivery_cleaned.csv`** afin d'être exploitées dans le tableau de bord.
    """)

    # Charger les données nettoyées
    df = load_csv("../data/cleaned/amazon_delivery_cleaned.csv")

    # Aperçu dans un expander
    with st.expander("Voir un aperçu du dataset (1000 lignes)"):
        st.dataframe(df.head(1000))

    # KPIs globaux
    st.markdown("### Indicateurs Clés Globaux")
    df['Order_Date'] = pd.to_datetime(df['Order_Date'])

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Livraisons", len(df))
    col2.metric("Retards (>120 min)", int(df["delivery_risk"].sum()))
    col3.metric("Délai Moyen", f"{df['Delivery_Time'].mean():.1f} min")
    col4.metric("Résilience Moyenne", f"{df['weather_traffic_resilience_score'].mean():.2f}")
    col5.metric('Plage Temporelle', f'{df['Order_Date'].min().year} - {df['Order_Date'].max().year}')

    tab1, tab2, tab3 = st.tabs(["Vue Globale", "Analyse Temporelle", "Heatmap"])

    with tab1:
        show_tab1(df)

    with tab2:
        show_tab2(df)

    with tab3:
        show_tab3(df)

    st.markdown("---")

    # Résumé
    st.info(f"""
    **Résumé de l'Analyse :**

    - **Nombre total de commandes analysées :** {len(df):,}
    - **Taux global de retard (>120 min) :** {df['delivery_risk'].mean():.2%}
    - **Plages horaires critiques :**
        - Heure de commande avec le plus fort taux de retard : `{df.groupby('Order_Hour')['delivery_risk'].mean().idxmax()}h`
        - Moment de la journée le plus risqué : `{df.groupby(df['Order_Hour'].apply(lambda h: 'Matin' if 6 <= h < 12 else 'Après-midi' if 12 <= h < 18 else 'Soir/Nuit'))['delivery_risk'].mean().idxmax()}`
    - **Contexte météo-trafic le plus critique :** `{df.groupby(['Weather', 'Traffic'])['delivery_risk'].mean().idxmax()}`
    - **Zone géographique la plus à risque :** `{df.groupby('Area')['area_risk_score'].mean().idxmax()}`
    - **Catégorie la plus fréquemment commandée :** `{df['Category'].mode()[0]}`
    """)

show()
