import streamlit as st
import base64
from modules import traffic, airline, railroad, shipping, supply_chain

st.set_page_config(
    page_title="Analyse des Risques - Résilience Chaîne Logistique",
    page_icon="assets/logo.png",
    layout="wide"
)

# ----------------------------------------
# FONCTION POUR ENCODER IMAGE
# ----------------------------------------
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# ----------------------------------------
# LOGO CLIQUABLE EN BASE64
# ----------------------------------------
logo_base64 = get_base64_of_bin_file("assets/logo.png")

st.sidebar.markdown(
    f"""
    <div style="text-align: center;">
        <a href="?page=home">
            <img src="data:image/png;base64,{logo_base64}" style="width: 120px; height: auto; display: block; margin: auto;">
        </a>
    </div>
    """,
    unsafe_allow_html=True
)

# ----------------------------------------
# SIDEBAR - NAVIGATION
# ----------------------------------------
st.sidebar.markdown(
    f"""
    <div style="text-align: center; margin-top: 10px;">
        <a href="?page=home" style="text-decoration: none; font-size: 22px; font-weight: bold; color: inherit;">
            Analyse de Risque Logistiques
        </a>
    </div>
    """,
    unsafe_allow_html=True
)

pages = {
    "🏠 Dashboard": "home",
    "🚗 Transport Routier": "traffic_accident",
    "✈️ Transport Aérien": "airline",
    "🚆 Transport Ferroviaire": "railroad",
    "🚢 Transport Maritime": "shipping",
    "📦 Analyse des Fournisseurs": "supply_chain"
}

selection = st.sidebar.radio("-", list(pages.keys()))

if "page" not in st.session_state:
    st.session_state["page"] = pages[selection]
else:
    st.session_state["page"] = pages[selection]

# ----------------------------------------
# ROUTAGE
# ----------------------------------------
if st.session_state["page"] == "home":
    st.title("Analyse de Risque - Résilience Chaîne Logistique")
    st.write("""
    Ce tableau de bord interactif aide à anticiper et visualiser les perturbations potentielles
    pour la continuité de la chaîne logistique.
    """)

elif st.session_state["page"] == "traffic_accident":
    traffic.show()

elif st.session_state["page"] == "airline":
    airline.show()

elif st.session_state["page"] == "railroad":
    railroad.show()

elif st.session_state["page"] == "shipping":
    shipping.show()

elif st.session_state["page"] == "supply_chain":
    supply_chain.show()
