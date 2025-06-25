import streamlit as st
import pandas as pd

@st.cache_data
def load_csv(filepath):
    """Charge un CSV et le met en cache pour améliorer les performances."""
    return pd.read_csv(filepath)

def apply_responsive(fig):
    fig.update_layout(
        autosize=True,
        width=None,
        height=500,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    return fig
