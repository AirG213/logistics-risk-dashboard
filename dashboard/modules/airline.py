from utils import load_csv, apply_responsive
import streamlit as st
import plotly.express as px

def show():
    st.markdown(
        """
        # ✈️ Analyse des Retards Aériens
        """
    )

    df = load_csv('../data/cleaned/airline_delay_cause_cleaned.csv')

    # Aperçu du CSV
    with st.expander('Voir un aperçu du fichier final nettoyé et enrichi (1000 lignes)'):
        st.dataframe(df.head(1000))

    # KPI
    col1, col2, col3, col4 = st.columns(4)
    col1.metric('Nombre de Vols', f'{int(df['arr_flights'].sum()):,}')
    col2.metric('Nombre de Retards', f'{int(df['arr_del15'].sum()):,}')
    col3.metric('Temps total de Retard (minutes)', f'{int(df['arr_delay'].sum()):,}')
    col4.metric('Plage Temporelle', f'{df['year'].min().astype(int)} - {df['year'].max().astype(int)}')

    col1.metric('Nombre de Vols Annulé', f'{int(df['arr_cancelled'].sum()):,}')
    col2.metric('Nombre de Vols Dérouté', f'{int(df['arr_diverted'].sum()):,}')

    ## Préparer les agrégats


    tab1, tab2 = st.tabs(['Vue Globale', 'Analyses Plage Temporelle'])
    with tab1:
        st.subheader("Total des retards par catégorie")

        # Colonnes représentant les catégories de retard
        delay_cols = [
            'carrier_ct',
            'weather_ct',
            'nas_ct',
            'security_ct',
            'late_aircraft_ct'
        ]

        # Vérifier que les colonnes existent dans le DataFrame
        if all(col in df.columns for col in delay_cols):
            delay_totals = df[delay_cols].sum().reset_index()
            delay_totals.columns = ['Cause', 'Total Retards']

            fig = px.bar(
                delay_totals,
                x='Cause',
                y='Total Retards',
                title='Total des retards par cause',
                text='Total Retards',
                labels={'Total Retards': 'Minutes de retard', 'Cause': 'Catégorie'},
                color='Cause',
                template='plotly_white'
            )

            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Certaines colonnes de retard sont manquantes dans le fichier.")

    with tab2:
        pass