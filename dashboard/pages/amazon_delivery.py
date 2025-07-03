import streamlit as st
import pandas as pd
import base64
from utils import load_csv, apply_responsive
import plotly.express as px
from sidebar import show_sidebar

show_sidebar()

def show_tab1(df):
    # Histogramme des temps de livraison
    st.markdown("### Distribution des Temps de Livraison (en minutes)")
    fig_hist = px.histogram(df, x="Delivery_Time", nbins=50, color_discrete_sequence=["#1f77b4"])
    apply_responsive(fig_hist)
    st.plotly_chart(fig_hist, use_container_width=True)

    st.markdown("---")

    # Top contextes à risque (Weather x Traffic)
    st.markdown("### Contextes les Plus à Risque (Météo & Trafic)")
    top_risks = (
        df.groupby(['Weather', 'Traffic'])['delivery_risk']
        .mean()
        .sort_values(ascending=False)
        .head(5)
        .reset_index()
    )
    st.dataframe(top_risks, hide_index=True, use_container_width=True)

    st.markdown("---")

    # Zones géographiques avec le plus de risques
    st.markdown("### Zones Géographiques à Risque")
    area_risks = (
        df.groupby('Area', as_index=False)['area_risk_score']
        .mean()
        .sort_values(by="area_risk_score", ascending=False)
    )
    st.dataframe(area_risks, hide_index=True, use_container_width=True)

    st.markdown("---")

    # Catégories les plus représentées
    st.markdown("### Catégories de Produits les plus Vendues")
    top_categories = (
        df['Category'].value_counts()
        .reset_index()
        .rename(columns={'index': 'Category', 'Category': 'Occurrences'})
    ).head(5)
    st.dataframe(top_categories, hide_index=True, use_container_width=True)

def show_tab2(df):
    df_time = df.copy()
    df_time["Order_Date"] = pd.to_datetime(df_time["Order_Date"], errors="coerce")
    df_time["Order_Hour"] = pd.to_datetime(df_time["Order_Time"], format="%H:%M:%S", errors="coerce").dt.hour
    df_time["Pickup_Hour"] = pd.to_datetime(df_time["Pickup_Time"], format="%H:%M:%S", errors="coerce").dt.hour
    df_time["DayOfWeek"] = df_time["Order_Date"].dt.day_name()

    # Bloc 1 — Volume global par heure
    st.subheader("Volume de Commandes par Heure de la Journée")
    fig_orders = px.histogram(df_time, x="Order_Hour", nbins=24, labels={"Order_Hour": "Heure"},
                              title="Nombre de commandes passées par heure",
                              color_discrete_sequence=["#006eff"])
    fig_orders.update_layout(margin=dict(l=0, r=0, t=40, b=0))
    apply_responsive(fig_orders)
    st.plotly_chart(fig_orders, use_container_width=True)

    st.markdown("---")

    # Bloc 2 — Temps de livraison moyen par heure
    st.subheader("Temps de Livraison selon l'Heure de Commande")
    fig_box = px.box(df_time, x="Order_Hour", y="Delivery_Time",
                     labels={"Order_Hour": "Heure", "Delivery_Time": "Temps de livraison (min)"},
                     title="Distribution des délais selon l'heure de la commande",
                     color_discrete_sequence=["#9b59b6"])
    fig_box.update_layout(margin=dict(l=0, r=0, t=40, b=0))
    apply_responsive(fig_box)
    st.plotly_chart(fig_box, use_container_width=True)

    st.markdown("---")

    # Bloc 3 — Risque de retard par heure
    st.subheader("Taux de Retard (>120min) par Heure")
    risk_by_hour = df_time.groupby("Order_Hour")["delivery_risk"].mean().reset_index()
    fig_risk_hour = px.line(risk_by_hour, x="Order_Hour", y="delivery_risk", markers=True,
                            labels={"delivery_risk": "Taux de retard"},
                            title="Proportion de retards selon l'heure de la commande",
                            color_discrete_sequence=["#e74c3c"])
    fig_risk_hour.update_layout(yaxis_tickformat=".0%", margin=dict(l=0, r=0, t=40, b=0))
    apply_responsive(fig_risk_hour)
    st.plotly_chart(fig_risk_hour, use_container_width=True)

    st.markdown("---")

    # Bloc 4 — Risque de retard par jour de la semaine
    st.subheader("Taux de Retard selon le Jour de la Semaine")
    risk_by_day = df_time.groupby("DayOfWeek")["delivery_risk"].mean().reindex([
        "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]).reset_index()
    fig_risk_day = px.bar(risk_by_day, x="DayOfWeek", y="delivery_risk",
                          labels={"delivery_risk": "Taux de retard"},
                          title="Retards moyens par jour de la semaine",
                          color_discrete_sequence=["#f39c12"])
    fig_risk_day.update_layout(yaxis_tickformat=".0%", margin=dict(l=0, r=0, t=40, b=0))
    apply_responsive(fig_risk_day)
    st.plotly_chart(fig_risk_day, use_container_width=True)

    st.markdown("---")

    # Bloc 5 — Comparaison matin vs soir
    st.subheader("Matin vs Soir : Comparaison du Taux de Retard")
    df_time["Period"] = df_time["Order_Hour"].apply(lambda h: "Matin (6h-12h)" if 6 <= h < 12 else
                                                              "Après-midi (12h-18h)" if 12 <= h < 18 else
                                                              "Soir/Nuit (18h-6h)")
    risk_by_period = df_time.groupby("Period")["delivery_risk"].mean().reindex([
        "Matin (6h-12h)", "Après-midi (12h-18h)", "Soir/Nuit (18h-6h)"]).reset_index()
    fig_risk_period = px.bar(risk_by_period, x="Period", y="delivery_risk",
                             labels={"delivery_risk": "Taux de retard"},
                             title="Taux de retard en fonction du moment de la journée",
                             color_discrete_sequence=["#1abc9c"])
    fig_risk_period.update_layout(yaxis_tickformat=".0%", margin=dict(l=0, r=0, t=40, b=0))
    apply_responsive(fig_risk_period)
    st.plotly_chart(fig_risk_period, use_container_width=True)

    st.markdown("---")

    # Bloc 6 — Évolution temporelle globale (par date)
    st.subheader("Évolution Globale du Taux de Retard")
    risk_by_date = df_time.groupby("Order_Date")["delivery_risk"].mean().reset_index()
    fig_date = px.line(risk_by_date, x="Order_Date", y="delivery_risk", markers=True,
                       labels={"delivery_risk": "Taux de retard"},
                       title="Évolution du risque de retard sur la période analysée",
                       color_discrete_sequence=["#2980b9"])
    fig_date.update_layout(yaxis_tickformat=".0%", margin=dict(l=0, r=0, t=40, b=0))
    apply_responsive(fig_date)
    st.plotly_chart(fig_date, use_container_width=True)

def show_tab3(df):
    # Météo × Trafic
    st.subheader("Carte des Risques — Météo x Trafic")
    risk_weather_traffic = df.pivot_table(index="Weather", columns="Traffic", values="delivery_risk", aggfunc="mean")
    fig1 = px.imshow(
        risk_weather_traffic,
        text_auto=".2f",
        color_continuous_scale="Reds",
        aspect="auto",
        labels=dict(color="Taux de retard"),
        title="Taux de retard (>120min) selon Météo et Trafic"
    )
    st.plotly_chart(fig1, use_container_width=True)
    apply_responsive(fig1)

    st.markdown("---")

    # Zone x Météo
    st.subheader("Carte des Risques — Zone x Météo")
    risk_area_weather = df.pivot_table(index="Weather", columns="Area", values="delivery_risk", aggfunc="mean")
    fig2 = px.imshow(
        risk_area_weather,
        text_auto=".2f",
        color_continuous_scale="Oranges",
        aspect="auto",
        labels=dict(color="Taux de retard"),
        title="Taux de retard selon Zone et Météo"
    )
    st.plotly_chart(fig2, use_container_width=True)
    apply_responsive(fig2)

    st.markdown("---")

    # Jour x Heure
    st.subheader("Carte des Risques — Jour x Heure de Commande")
    df["Order_Hour"] = pd.to_datetime(df["Order_Time"], format="%H:%M:%S", errors="coerce").dt.hour
    df["DayOfWeek"] = pd.to_datetime(df["Order_Date"], format="%Y-%m-%d", errors="coerce").dt.day_name()
    ordered_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    risk_day_hour = df.pivot_table(index="DayOfWeek", columns="Order_Hour", values="delivery_risk", aggfunc="mean")
    risk_day_hour = risk_day_hour.reindex(ordered_days)
    fig3 = px.imshow(
        risk_day_hour,
        text_auto=False,
        color_continuous_scale="Purples",
        aspect="auto",
        labels=dict(color="Taux de retard"),
        title="Retards selon le Jour et l'Heure de Commande"
    )
    st.plotly_chart(fig3, use_container_width=True)
    apply_responsive(fig3)

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
