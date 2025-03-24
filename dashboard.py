import streamlit as st
import pandas as pd
import plotly.express as px
import re
from main import analyze_brand

st.set_page_config(page_title="Brand Sentiment Dashboard", layout="wide")
st.title("🔍 Reddit Brand Analysis Tool")

# Session state initialization
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame()
if 'topics' not in st.session_state:
    st.session_state.topics = []

# Sidebar controls
with st.sidebar:
    st.header("Analysis Parameters")
    brand_input = st.text_input("Brand Name", "Apple")
    brand_name = re.sub(r'[^\w\s-]', '', brand_input).strip()
    subreddits = st.multiselect(
        "Subreddits to Monitor",
        ["technology", "business", "marketing", "startups", "games"],
        default=["technology", "business"]
    )
    analysis_days = st.slider("Analysis Period (days)", 1, 90, 30)
    run_analysis = st.button("Analyze Brand Sentiment")

# Main display
if run_analysis:
    with st.spinner(f"Analyzing {brand_name} in {', '.join(subreddits)}..."):
        st.session_state.df, st.session_state.topics = analyze_brand(
            brand_name, subreddits
        )

if not st.session_state.df.empty:
    df = st.session_state.df
    
    # Sentiment Overview
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Sentiment Distribution")
        fig = px.pie(df, names='sentiment', 
                    color_discrete_map={
                        'NEGATIVE': '#EF553B',
                        'NEUTRAL': '#636EFA',
                        'POSITIVE': '#00CC96'
                    })
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Sentiment Timeline")
        df['date'] = pd.to_datetime(df['created_utc'], unit='s')
        weekly = df.groupby([pd.Grouper(key='date', freq='W'), 'sentiment']).size().unstack()
        fig = px.line(weekly, labels={'value': 'Posts'})
        st.plotly_chart(fig, use_container_width=True)
    
    # Topic Modeling
    st.subheader("Key Discussion Topics")
    if st.session_state.topics:
        cols = st.columns(len(st.session_state.topics))
        for idx, (col, topic) in enumerate(zip(cols, st.session_state.topics)):
            col.metric(f"Topic {idx+1}", topic)
    else:
        st.warning("No significant topics identified")
    
    # Raw Data
    st.subheader("Recent Mentions")
    st.dataframe(
        df[['date', 'sentiment', 'subreddit', 'title', 'url', 'score']],
        column_config={
            "url": st.column_config.LinkColumn("Post Link"),
            "score": st.column_config.NumberColumn("Upvotes")
        },
        hide_index=True,
        use_container_width=True
    )
elif run_analysis:
    st.error(f"No discussions found for {brand_name} in selected subreddits")
else:
    st.info("Enter a brand name and select subreddits to begin analysis")