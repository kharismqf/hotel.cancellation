import streamlit as st
from streamlit_option_menu import option_menu

# Import fungsi halaman dari folder src
from src.overview import show_overview
from src.eda import show_eda
from src.predict import show_predict_page
from src.aboutme import show_creator

# Set page config
st.set_page_config(page_title="Hotel Cancellation Dashboard", layout="wide")

# Sidebar menu navigation
with st.sidebar:
    page = option_menu(
        menu_title="Main Menu",
        options=[
            "Understand the Data",
            "Explore The Data",
            "Try the Model",
            "Meet the Creator"
        ],
        icons=["bar-chart", "graph-up", "cpu", "person-circle"],
        default_index=0
    )

# Debug info (opsional, bisa dihapus jika sudah yakin)
st.write(f"✅ Current page: {page}")

# Routing halaman
if page == "Understand the Data":
    show_overview()
elif page == "Explore The Data":
    show_eda()
elif page == "Try the Model":
    show_predict_page()
elif page == "Meet the Creator":
    show_creator()
