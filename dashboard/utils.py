import streamlit as st
import pandas as pd

@st.cache_data
def load_csv(filepath):
    """Charge un CSV et le met en cache pour améliorer les performances."""
    return pd.read_csv(filepath)