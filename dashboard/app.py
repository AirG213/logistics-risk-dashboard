import streamlit as st
from streamlit_option_menu import option_menu
import base64
from modules import traffic, airline, railroad, shipping, supply_chain, amazon_delivery

st.set_page_config(
    page_title='Analyse des Risques - Résilience Chaîne Logistique',
    page_icon='assets/logo.png',
    layout='wide'
)

# ----------------------------------------
# FONCTION POUR ENCODER IMAGE
# ----------------------------------------
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# ----------------------------------------
# PAGE D'ACCUEIL
# ----------------------------------------
def show_home():
    st.title('Analyse de Risque - Résilience Chaîne Logistique')
    st.write("""
    Ce tableau de bord interactif aide à anticiper et visualiser les perturbations potentielles
    pour la continuité de la chaîne logistique.
    """)

# ----------------------------------------
# SIDEBAR - NAVIGATION
# ----------------------------------------
logo_base64 = get_base64_of_bin_file('assets/logo.png')

st.sidebar.markdown(
    f"""
    <div>
        <a href="?page=home">
            <img src="data:image/png;base64,{logo_base64}" style="width: 120px; height: auto; display: block; margin: auto;">
        </a>
    </div>
    <div style="text-align: center; margin-bottom: 20px;">
        <a href="?page=home" style="text-decoration: none; font-size: 22px; font-weight: bold; color: inherit;">
            Analyse de Risque Logistiques
        </a>
    </div>
    """,
    unsafe_allow_html=True
)

PAGES = {
    '🏠 Dashboard': show_home,
    '🚗 Transport Routier': traffic.show,
    '✈️ Transport Aérien': airline.show,
    '🚆 Transport Ferroviaire' : railroad.show,
    '🚢 Transport Maritime': shipping.show,
    '📦 Fournisseurs': supply_chain.show,
    '📬 Livraison Amazon': amazon_delivery.show
}

with st.sidebar:
    selected_label = option_menu(
        None,
        ['🏠 Dashboard', '---'] + list(PAGES.keys())[1:],
        default_index=0
    )

PAGES.get(selected_label, show_home)()