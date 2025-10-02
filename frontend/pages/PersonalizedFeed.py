import streamlit as st
from utils.api_client import recommend_for_user, send_feedback
from components.article_card import article_card


def app():
    st.title("Personalized Feed")
    user_id = st.text_input("User ID", value="user_1")
    if st.button("Get Recommendations"):
        with st.spinner("Loading recommendations..."):
            recs = recommend_for_user(user_id)
            for a in recs:
                article_card(a, show_feedback=True, feedback_callback=lambda article_id, reward: send_feedback(user_id, article_id, reward))
