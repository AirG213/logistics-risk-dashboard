import streamlit as st
from streamlit_option_menu import option_menu
from modules import traffic, airline, railroad, shipping, supply_chain, amazon_delivery, home
from utils import load_csv, get_base64, apply_responsive
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title='Analyse des Risques - Résilience Chaîne Logistique',
    page_icon='assets/logo.png',
    layout='wide'
)

# Chargement de chaque dataset
df_traffic = load_csv("../data/cleaned/usa_accidents_traffic_cleaned.csv")
df_airline = load_csv("../data/cleaned/airline_delay_cause_cleaned.csv")
df_railroad = load_csv("../data/cleaned/railroad_accident_cleaned.csv")
df_shipping = load_csv("../data/cleaned/shipping_accidents_cleaned.csv")
df_supply_chain = load_csv("../data/cleaned/supply_chain_cleaned.csv")
df_amazon = load_csv("../data/cleaned/amazon_delivery_cleaned.csv")

# ----------------------------------------
# SIDEBAR - NAVIGATION
# ----------------------------------------
get_base64 = get_base64('assets/logo.png')

st.sidebar.markdown(
    f"""
    <div>
        <a href="?page=home">
            <img src="data:image/png;base64,{get_base64}" style="width: 120px; height: auto; display: block; margin: auto;">
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
    '🏠 Dashboard': home.show,
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

if selected_label == '🏠 Dashboard':
    home.show(df_traffic, df_airline, df_railroad, df_shipping)
else:
    PAGES[selected_label]()