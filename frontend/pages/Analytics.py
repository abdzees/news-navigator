import streamlit as st
import pandas as pd
import plotly.express as px
from utils.api_client import get_feedback_stats


def app():
    st.title("Analytics")
    stats = get_feedback_stats()
    if not stats:
        st.info("No feedback data available yet.")
        return
    df = pd.DataFrame(stats)
    fig = px.bar(df, x='category', y='count', color='avg_reward')
    st.plotly_chart(fig, use_container_width=True)
