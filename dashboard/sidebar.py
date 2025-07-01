import streamlit as st
from utils import get_base64
import streamlit.components.v1 as components

def show_sidebar():
    # Injection en JavaScript pour cacher l'élément avant le rendu HTML
    components.html(
        """
        <script>
        const waitForSidebar = setInterval(() => {
            const nav = window.parent.document.querySelector('[data-testid="stSidebarNav"]');
            if (nav) {
                nav.style.display = 'none';
                clearInterval(waitForSidebar);
            }
        }, 1);
        </script>
        """,
        height=0,
        width=0
    )

    st.set_page_config(
        page_title='Analyse des Risques - Résilience Chaîne Logistique',
        page_icon='assets/logo.png',
        layout='wide'
    )

    base_img = get_base64('assets/logo.png')

    st.sidebar.markdown(
        f"""
        <div>
            <a href="/">
                <img src="data:image/png;base64,{base_img}" style="width: 120px; height: auto; display: block; margin: auto;">
            </a>
        </div>
        <div style="text-align: center; margin-bottom: 40px;">
            <a href="/" style="text-decoration: none; font-size: 22px; font-weight: bold; color: inherit;">
                Analyse de Risque Logistiques
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )

    PAGES = {
        '🏠 Dashboard': 'app.py',
        '🚗 Transport Routier': 'pages/traffic.py',
        '✈️ Transport Aérien': 'pages/airline.py',
        '🚆 Transport Ferroviaire' : 'pages/railroad.py',
        '🚢 Transport Maritime': 'pages/shipping.py',
        '📦 Fournisseurs': 'pages/supply_chain.py',
        '📬 Livraison Amazon': 'pages/amazon_delivery.py'
    }

    with st.sidebar:
        for page_name, page_file in PAGES.items():
            st.page_link(page_file, label=page_name)
