from utils import load_csv, apply_responsive
import streamlit as st
import plotly.express as px

def show():
    st.markdown(
        """
        # 🚢 Analyse des Accidents Maritimes
        """
    )

    df = load_csv('../data/cleaned/shipping_accidents_cleaned.csv')

    # Aperçu du CSV
    with st.expander('Voir un aperçu du fichier final nettoyé et enrichi (1000 lignes)'):
        st.dataframe(df.head(1000))

    # KPI
    total = df.shape[0]

    col1, col2 = st.columns(2)
    col1.metric('Total Accidents', f'{total:,}')
    col2.metric('Plage Temporelle', f'{df["Year"].min().astype(int)} - {df["Year"].max().astype(int)}')

    # Préparer les agrégats
    risk_summary = df['Acc_Type'].value_counts().reset_index()
    risk_summary.columns = ['Risk_Category', 'Count']
    risk_summary['Proportion (%)'] = (risk_summary['Count'] / total * 100).round(2).astype(str) + '%'

    risk_summary_2 = df['Location'].value_counts().reset_index()
    risk_summary_2.columns = ['Location', 'Count']

    sunburst_data = df.groupby(['Acc_Type', 'Location']).size().reset_index(name='Count')

    tab1, tab2 = st.tabs(['Vue Globale', 'Analyses Plage Temporelle'])
    with tab1:

        st.subheader('Vue Globale des Accidents Maritimes')

        fig_bar = px.bar(
            risk_summary,
            x='Count',
            y='Risk_Category',
            orientation='h',
            text='Proportion (%)',
            title='Répartition des Accidents par Type',
            labels={'Risk_Category': "Type d'Accident", 'Count': "Nombre d'Accidents"},
            color='Risk_Category',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        st.plotly_chart(apply_responsive(fig_bar), use_container_width=True)

        fig_pie = px.pie(
            risk_summary_2,
            values='Count',
            names='Location',
            title='Répartition des Accidents par Lieu',
            labels={'Location': 'Lieu', 'Count': 'Nombre d\'Accidents'},
            color='Location',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        st.plotly_chart(apply_responsive(fig_pie), use_container_width=True)

        fig_sunburst = px.sunburst(
            sunburst_data,
            path=['Location', 'Acc_Type'],
            values='Count',
            title='Hiérarchie des Accidents par Type et Lieu',
            labels={'Location': 'Lieu', 'Acc_Type': "Type d'Accident"},
            color='Acc_Type',
            color_discrete_sequence=px.colors.qualitative.Set2,
        )
        st.plotly_chart(apply_responsive(fig_sunburst), use_container_width=True)

    with tab2:
        fig = px.scatter_map(df, lat='Latitude', lon='Longitude', hover_name='Unique_ID', hover_data=['Acc_Type'],
                        color_discrete_sequence=['red'], zoom=3, height=300, animation_frame='Year', animation_group='Unique_ID')
        fig.update_layout(map_style='basic')
        fig.update_layout(margin={'r':0,'t':0,'l':0,'b':0})
        st.plotly_chart(apply_responsive(fig), use_container_width=True)
