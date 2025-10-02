import streamlit as st


def feedback_buttons(article_id: int, callback):
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button('Like', key=f"like_{article_id}"):
            callback(article_id, 1.0)
    with col2:
        if st.button('Dislike', key=f"dislike_{article_id}"):
            callback(article_id, 0.0)
