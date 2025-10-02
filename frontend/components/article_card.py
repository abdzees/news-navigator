import streamlit as st


def article_card(article: dict, show_feedback: bool = False, feedback_callback=None):
    st.subheader(article.get('title'))
    if article.get('source'):
        st.caption(article.get('source'))
    if article.get('description'):
        st.write(article.get('description'))
    if article.get('url'):
        st.markdown(f"[Read more]({article.get('url')})")
    if show_feedback and feedback_callback:
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button('Like', key=f"like_{article.get('id')}"):
                feedback_callback(article.get('id'), 1.0)
        with col2:
            if st.button('Dislike', key=f"dislike_{article.get('id')}"):
                feedback_callback(article.get('id'), 0.0)
