from utils import load_csv, apply_responsive
import streamlit as st
import plotly.express as px
import pandas as pd
from sidebar import show_sidebar

show_sidebar()

color_map = {
    'Retard compagnie aérienne': '#636EFA',
    'Retard météo': '#EF553B',
    'Retard contrôle aérien (NAS)': '#00CC96',
    'Retard sécurité': '#AB63FA',
    'Retard avion précédent': '#FFA15A'
}

def show_tab1(df):
    st.subheader("Répartition des retards par catégorie")

    delay_cols = [
        'carrier_ct',
        'weather_ct',
        'nas_ct',
        'security_ct',
        'late_aircraft_ct'
    ]

    readable_labels = {
        'carrier_ct': 'Retard compagnie aérienne',
        'weather_ct': 'Retard météo',
        'nas_ct': 'Retard contrôle aérien (NAS)',
        'security_ct': 'Retard sécurité',
        'late_aircraft_ct': 'Retard avion précédent'
    }

    if all(col in df.columns for col in delay_cols):
        delay_totals = df[delay_cols].sum().astype(int).reset_index()
        delay_totals.columns = ['Cause', 'Total Retards']

        delay_totals['Cause'] = delay_totals['Cause'].map(readable_labels)

        delay_totals['Total Formatté'] = delay_totals['Total Retards'].apply(lambda x: f"{x:,}")
        delay_totals_sorted = delay_totals.sort_values(by='Total Retards', ascending=False)

        fig = px.bar(
            delay_totals_sorted,
            x='Cause',
            y='Total Retards',
            title='Nombre de retard par catégorie',
            text='Total Formatté',
            labels={'Total Retards': 'Minutes de retard', 'Cause': 'Catégorie'},
            color='Cause',
            color_discrete_map=color_map,
            template='plotly_white'
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Certaines colonnes de retard sont manquantes dans le fichier.")

    delay_time_cols = [
        'carrier_delay',
        'weather_delay',
        'nas_delay',
        'security_delay',
        'late_aircraft_delay'
    ]

    readable_time_labels = {
        'carrier_delay': 'Retard compagnie aérienne',
        'weather_delay': 'Retard météo',
        'nas_delay': 'Retard contrôle aérien (NAS)',
        'security_delay': 'Retard sécurité',
        'late_aircraft_delay': 'Retard avion précédent'
    }

    if all(col in df.columns for col in delay_time_cols):
        delay_times = df[delay_time_cols].sum().astype(int).reset_index()
        delay_times.columns = ['Cause', 'Minutes de retard']
        delay_times['Cause'] = delay_times['Cause'].map(readable_time_labels)

        # Formatage des minutes
        delay_times['Minutes formatées'] = delay_times['Minutes de retard'].apply(lambda x: f"{x:,}")
        delay_times_sorted = delay_times.sort_values(by='Minutes de retard', ascending=False)

        fig_time = px.bar(
            delay_times_sorted,
            x='Cause',
            y='Minutes de retard',
            title='Temps total de retard par catégorie (en minutes)',
            text='Minutes formatées',
            labels={'Minutes de retard': 'Minutes', 'Cause': 'Catégorie'},
            color='Cause',
            color_discrete_map=color_map,
            template='plotly_white'
        )
        st.plotly_chart(fig_time, use_container_width=True)
    else:
        st.warning("Les colonnes de temps de retard par cause sont manquantes.")

    st.markdown("---")

    st.subheader("Top 10 des aéroports avec le plus fort taux de retard")

    if {'airport_name', 'arr_del15', 'arr_flights'}.issubset(df.columns):
        airport_stats = (
            df.groupby('airport_name', as_index=False)[['arr_del15', 'arr_flights']]
            .sum()
        )

        # Éviter la division par 0
        airport_stats = airport_stats[airport_stats['arr_flights'] > 0]

        # Calcul du taux de retard
        airport_stats['Taux de retard (%)'] = (airport_stats['arr_del15'] / airport_stats['arr_flights']) * 100

        # Formatage
        airport_stats['arr_del15'] = airport_stats['arr_del15'].astype(int)
        airport_stats['arr_flights'] = airport_stats['arr_flights'].astype(int)
        airport_stats['Taux de retard (%)'] = airport_stats['Taux de retard (%)'].round(2)

        # Top 10 par taux décroissant
        top_airports = airport_stats.sort_values(by='Taux de retard (%)', ascending=False).head(10).reset_index()
        top_airports.index = top_airports.index + 1
        del top_airports['index']

        # Affichage
        st.dataframe(top_airports.rename(columns={
            'airport_name': 'Aéroport',
            'arr_del15': 'Vols retardés',
            'arr_flights': 'Vols totaux'
        }), use_container_width=True)

    else:
        st.warning("Les colonnes nécessaires ('airport_name', 'arr_del15', 'arr_flights') sont manquantes.")

    st.markdown("---")

    st.subheader("Top 10 des compagnies avec le plus fort taux de retard")

    if {'carrier_name', 'arr_del15', 'arr_flights'}.issubset(df.columns):
        airport_stats = (
            df.groupby('carrier_name', as_index=False)[['arr_del15', 'arr_flights']]
            .sum()
        )

        # Éviter la division par 0
        airport_stats = airport_stats[airport_stats['arr_flights'] > 0]

        # Calcul du taux de retard
        airport_stats['Taux de retard (%)'] = (airport_stats['arr_del15'] / airport_stats['arr_flights']) * 100

        # Formatage
        airport_stats['arr_del15'] = airport_stats['arr_del15'].astype(int)
        airport_stats['arr_flights'] = airport_stats['arr_flights'].astype(int)
        airport_stats['Taux de retard (%)'] = airport_stats['Taux de retard (%)'].round(2)

        # Top 10 par taux décroissant
        top_airports = airport_stats.sort_values(by='Taux de retard (%)', ascending=False).head(10).reset_index()
        top_airports.index = top_airports.index + 1
        del top_airports['index']

        # Affichage
        st.dataframe(top_airports.rename(columns={
            'carrier_name': 'Compagnie',
            'arr_del15': 'Vols retardés',
            'arr_flights': 'Vols totaux'
        }), use_container_width=True)

    else:
        st.warning("Les colonnes nécessaires ('carrier_name', 'arr_del15', 'arr_flights') sont manquantes.")

def show_tab2(df):
    st.subheader("Temps moyen de retard par vol retardé, selon la catégorie (par an)")

    delay_time_cols = {
        'carrier_delay': 'Retard compagnie aérienne',
        'weather_delay': 'Retard météo',
        'nas_delay': 'Retard contrôle aérien (NAS)',
        'security_delay': 'Retard sécurité',
        'late_aircraft_delay': 'Retard avion précédent'
    }

    if 'arr_del15' in df.columns and 'year' in df.columns and all(col in df.columns for col in delay_time_cols):
        df_valid = df[df['arr_del15'] > 0].copy()

        # Calculer pour chaque cause la colonne "minutes par vol retardé"
        for col in delay_time_cols:
            df_valid[f'{col}_per_delayed_flight'] = df_valid[col] / df_valid['arr_del15']

        # Préparer les données pour animation : moyenne par année
        result_frames = []
        for year, group in df_valid.groupby('year'):
            averages = {
                'year': year
            }
            for col, label in delay_time_cols.items():
                mean_val = group[f'{col}_per_delayed_flight'].mean()
                averages['Cause'] = label
                averages['Temps moyen (min)'] = round(mean_val, 2)
                result_frames.append(averages.copy())

        animated_df = pd.DataFrame(result_frames)
        animated_df['Texte'] = animated_df['Temps moyen (min)'].apply(lambda x: f"{x:.2f}")
        animated_df_sorted = animated_df.sort_values(by='Temps moyen (min)', ascending=False)

        fig = px.bar(
            animated_df_sorted,
            y='Cause',
            x='Temps moyen (min)',
            animation_frame='year',
            orientation='h',
            color='Cause',
            color_discrete_map=color_map,
            text='Texte',
            template='plotly_white',
            range_x=[0,30]
        )

        fig.update_traces(textposition='outside')
        fig.update_layout(yaxis_title='', xaxis_title='Minutes')

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Certaines colonnes nécessaires sont manquantes.")

    st.markdown("---")

    st.subheader("Évolution du taux de retard dans le temps")

    if 'arr_del15' in df.columns and 'arr_flights' in df.columns and 'year' in df.columns:
        # Aggrégation par année
        delay_rate_df = (
            df.groupby('year')[['arr_del15', 'arr_flights']]
            .sum()
            .reset_index()
        )

        delay_rate_df['Taux de retard (%)'] = (delay_rate_df['arr_del15'] / delay_rate_df['arr_flights']) * 100
        delay_rate_df['Taux de retard (%)'] = delay_rate_df['Taux de retard (%)'].round(2)

        fig_delay_rate = px.line(
            delay_rate_df,
            x='year',
            y='Taux de retard (%)',
            markers=True,
            title='Taux de retard (%) par an',
            labels={'year': 'Année', 'Taux de retard (%)': 'Taux de retard (%)'},
            template='plotly_white'
        )

        fig_delay_rate.update_layout(xaxis=dict(dtick=1))
        st.plotly_chart(fig_delay_rate, use_container_width=True)

    else:
        st.warning("Colonnes 'arr_del15', 'arr_flights' ou 'year' manquantes.")

def show_tab3(df):
    st.subheader("Corrélation entre les durées de retard (en minutes)")

    delay_time_cols = {
        'carrier_delay': 'Compagnie aérienne',
        'weather_delay': 'Météo',
        'nas_delay': 'Contrôle aérien (NAS)',
        'security_delay': 'Sécurité',
        'late_aircraft_delay': 'Avion précédent'
    }

    if all(col in df.columns for col in delay_time_cols):
        corr_df = df[list(delay_time_cols)].corr()
        corr_df.columns = [delay_time_cols[c] for c in corr_df.columns]
        corr_df.index = [delay_time_cols[c] for c in corr_df.index]

        fig_corr1 = px.imshow(
            corr_df.round(2),
            text_auto=True,
            color_continuous_scale='Blues',
            title="Corrélation entre les temps de retard (en minutes)",
            labels=dict(color="Corrélation"),
            aspect="auto"
        )
        st.plotly_chart(fig_corr1, use_container_width=True)
    else:
        st.warning("Colonnes de durée de retard manquantes.")

    st.markdown("---")
    st.subheader("Corrélation entre les fréquences de retard (nombre de cas)")

    delay_count_cols = {
        'carrier_ct': 'Compagnie aérienne',
        'weather_ct': 'Météo',
        'nas_ct': 'Contrôle aérien (NAS)',
        'security_ct': 'Sécurité',
        'late_aircraft_ct': 'Avion précédent'
    }

    if all(col in df.columns for col in delay_count_cols):
        corr_df2 = df[list(delay_count_cols)].corr()
        corr_df2.columns = [delay_count_cols[c] for c in corr_df2.columns]
        corr_df2.index = [delay_count_cols[c] for c in corr_df2.index]

        fig_corr2 = px.imshow(
            corr_df2.round(2),
            text_auto=True,
            color_continuous_scale='Oranges',
            title="Corrélation entre les fréquences de retard (nombre de cas)",
            labels=dict(color="Corrélation"),
            aspect="auto"
        )
        st.plotly_chart(fig_corr2, use_container_width=True)
    else:
        st.warning("Colonnes de comptage de retard manquantes.")

    with st.expander("💡 Interprétation de la corrélation entre les causes"):
        st.markdown(f"""
        - Une **forte corrélation positive** entre certaines causes indique qu'elles surviennent souvent ensemble.
        Exemple : les retards dus à **l'avion précédent** sont fortement liés aux **retards de la compagnie aérienne**, ce qui suggère des effets en chaîne internes.
        - À l'inverse, une **faible ou nulle corrélation** entre deux causes (comme **météo** et **sécurité**) signifie qu'elles sont généralement indépendantes.

        - La comparaison entre **temps de retard** et **nombre de retards** permet d'identifier les causes **fréquentes** mais peu longues, ou **rares** mais très **pénalisantes** en durée.
        """)

def show():
    st.markdown(
        """
        # ✈️ Analyse des Retards Aériens
        """
    )

    st.markdown("""
    ### Contexte et Source des Données
    Ce module repose sur le dataset **[USA Airline Delay Cause - Kaggle](https://www.kaggle.com/datasets/ryanjt/airline-delay-cause)** :
    - **Domaine :** Transport aérien américain
    - **Format :** CSV (nettoyé)
    - **Description :** Données sur les vols domestiques américains, incluant les retards de 15 minutes ou plus, la durée des retards, ainsi que la répartition des causes de retard (proratisée selon les minutes de retard attribuées à chaque cause). Les données sont arrondies et peuvent ne pas correspondre exactement au total.
    - **Pourquoi ce choix ? :** Permet d'identifier les causes principales de retard dans les opérations aériennes domestiques.
    """)

    df = load_csv('../data/cleaned/airline_delay_cause_cleaned.csv')

    # Aperçu du CSV
    with st.expander('Voir un aperçu du dataset (1000 lignes)'):
        st.dataframe(df.head(1000))

    # KPI
    col1, col2, col3 = st.columns(3)
    col1.metric('Nombre de Vols', f'{int(df['arr_flights'].sum()):,}')
    col2.metric('Nombre de Retards', f'{int(df['arr_del15'].sum()):,}')
    col3.metric('Temps total de Retard (minutes)', f'{int(df['arr_delay'].sum()):,}')

    col1.metric('Nombre de Vols Annulé', f'{int(df['arr_cancelled'].sum()):,}')
    col2.metric('Nombre de Vols Dérouté', f'{int(df['arr_diverted'].sum()):,}')
    col3.metric('Plage Temporelle', f'{df['year'].min().astype(int)} - {df['year'].max().astype(int)}')

    tab1, tab2, tab3 = st.tabs(['Vue Globale', 'Analyses Temporelle', 'Heatmap'])
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
    - **19,08% des vols** ont enregistré un retard.
    - **30,35% des retards** sont dus à **l'arrivée tardive d'un vol précédent** utilisant le même avion.
    - Les autres causes principales de retard sont liées à **la compagnie aérienne elle-même** et au **Système National de l'Aviation (NAS)**.
    - Les **aéroports les plus impactés** affichent des taux de retard compris entre **30% et 40%**.
    - Les **compagnies aériennes les moins ponctuelles** présentent des taux de retard allant de **20% à 25%**.
    - Le **taux de retard global** reste **relativement stable autour de 20%** au fil des années.
    """)

show()
