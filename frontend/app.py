import streamlit as st
from pages import Home, PersonalizedFeed, Analytics

PAGES = {
    "Home": Home,
    "Personalized Feed": PersonalizedFeed,
    "Analytics": Analytics,
}

st.set_page_config(page_title="News Navigator", layout="wide")

st.sidebar.title("News Navigator")
page = st.sidebar.radio("Go to", list(PAGES.keys()))

PAGES[page].app()
