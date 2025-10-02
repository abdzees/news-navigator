import streamlit as st
from components.article_card import article_card
from utils.api_client import fetch_articles


def app():
    st.title("Welcome to News Navigator")
    st.write("Choose a category or enter a search query to fetch latest headlines.")

    category = st.selectbox("Category", ["", "technology", "business", "politics", "sports", "science", "health", "entertainment"])
    query = st.text_input("Or search")
    if st.button("Fetch Articles"):
        q = query if query else category
        with st.spinner("Fetching..."):
            articles = fetch_articles(q)
            for a in articles:
                article_card(a)
