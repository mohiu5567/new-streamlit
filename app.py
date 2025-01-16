
```python
import streamlit as st
import plotly.express as px
from datetime import datetime
from utils import (
    setup_reddit,
    analyze_migration_patterns,
    create_migration_flow_chart
)
from config import DEFAULT_POST_LIMIT, DEFAULT_FUZZY_THRESHOLD, DEFAULT_GDP_YEAR

# Set page config
st.set_page_config(
    page_title="Global Migration Pattern Analysis",
    page_icon="🌍",
    layout="wide"
)

# Add custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stPlotlyChart {
        background-color: white;
        border-radius: 5px;
        padding: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    st.title("🌍 Global Migration Pattern Analysis")
    st.write("Analysis of migration patterns based on r/IWantOut subreddit")
    
    # Initialize Reddit client
    reddit = setup_reddit()
    if not reddit:
        st.error("Unable to connect to Reddit API. Please check the configuration.")
        return
    
    # Sidebar settings
    with st.sidebar:
        st.title("⚙️ Analysis Settings")
        post_limit = st.slider("Number of posts", 100, 1000, DEFAULT_POST_LIMIT)
        fuzzy_threshold = st.slider("Matching threshold", 60, 100, DEFAULT_FUZZY_THRESHOLD)
        gdp_year = st.selectbox("GDP Year", range(2022, 2015, -1), index=0)
    
    # Run analysis
    with st.spinner('Analyzing migration patterns...'):
        result = analyze_migration_patterns(reddit, post_limit, fuzzy_threshold, gdp_year)
    
    if result:
        data, raw_posts = result['data'], result['raw_posts']
        
        # Create tabs
        tab1, tab2, tab3 = st.tabs(["📊 Analysis", "🌊 Migration Flow", "📝 Raw Data"])
        
        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                fig_source = px.scatter(
                    data,
                    x='gdp_per_capita',
                    y='leaving_mentions',
                    text='country',
                    title='Countries People Want to Leave vs GDP per Capita',
                    log_x=True
                )
                st.plotly_chart(fig_source, use_container_width=True)
            
            with col2:
                fig_dest = px.scatter(
                    data,
                    x='gdp_per_capita',
                    y='moving_to_mentions',
                    text='country',
                    title='Desired Destination Countries vs GDP per Capita',
                    log_x=True
                )
                st.plotly_chart(fig_dest, use_container_width=True)
        
        with tab2:
            st.plotly_chart(create_migration_flow_chart(data), use_container_width=True)
        
        with tab3:
            st.dataframe(data)
            
            st.download_button(
                label="Download Data as CSV",
                data=data.to_csv(index=False),
                file_name=f"migration_analysis_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )

if __name__ == "__main__":
    main()
```
