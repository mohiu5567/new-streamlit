# File structure for your GitHub repository:

requirements.txt:
```
streamlit==1.32.0
praw==7.7.1
pandas==2.2.0
numpy==1.26.3
fuzzywuzzy==0.18.0
python-Levenshtein==0.23.0
wbgapi==1.0.3
plotly==5.18.0
python-dotenv==1.0.0
```

.gitignore:
```
.env
__pycache__/
*.pyc
.DS_Store
```

.env:
```
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USER_AGENT=migration_analysis_bot
```

config.py:
```python
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Reddit API credentials
REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
REDDIT_USER_AGENT = os.getenv('REDDIT_USER_AGENT')

# Analysis settings
DEFAULT_POST_LIMIT = 500
DEFAULT_FUZZY_THRESHOLD = 80
DEFAULT_GDP_YEAR = 2022
```

utils.py:
```python
import praw
import pandas as pd
import numpy as np
import re
from fuzzywuzzy import process
import wbgapi as wb
import streamlit as st
from config import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT

def setup_reddit():
    try:
        return praw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            user_agent=REDDIT_USER_AGENT
        )
    except Exception as e:
        st.error(f"Error setting up Reddit API: {str(e)}")
        return None

@st.cache_data(ttl=3600)
def get_iwantout_posts(reddit, limit=500):
    try:
        subreddit = reddit.subreddit('IWantOut')
        posts = []
        
        for submission in subreddit.new(limit=limit):
            posts.append({
                'title': submission.title,
                'created_utc': submission.created_utc,
                'url': f"https://reddit.com{submission.permalink}",
                'score': submission.score
            })
        
        df = pd.DataFrame(posts)
        df['created_date'] = pd.to_datetime(df['created_utc'], unit='s')
        return df
    except Exception as e:
        st.error(f"Error fetching Reddit posts: {str(e)}")
        return pd.DataFrame()

def extract_countries(title):
    try:
        pattern = r'(?i).*?([a-z\s]+)\s*-+>\s*([a-z\s]+)'
        match = re.search(pattern, title)
        
        if match:
            source = match.group(1).strip()
            destination = match.group(2).strip()
            return pd.Series([source, destination])
        return pd.Series([None, None])
    except Exception as e:
        return pd.Series([None, None])

@st.cache_data(ttl=86400)
def get_gdp_data(year):
    try:
        gdp_data = wb.data.DataFrame('NY.GDP.PCAP.CD', time=year, labels=True)
        gdp_data = gdp_data.reset_index()
        gdp_data = gdp_data.rename(columns={
            'economy': 'country',
            f'YR{year}': 'gdp_per_capita'
        })
        return gdp_data[['country', 'gdp_per_capita']].dropna()
    except Exception as e:
        st.error(f"Error fetching World Bank data: {str(e)}")
        return pd.DataFrame()

def analyze_migration_patterns(reddit, post_limit, fuzzy_threshold, gdp_year):
    # [Keep the same analyze_migration_patterns function from previous code]
    pass

def create_migration_flow_chart(data):
    # [Keep the same create_migration_flow_chart function from previous code]
    pass
```

app.py:
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

README.md:
```markdown
# Migration Pattern Analysis App

This Streamlit app analyzes migration patterns based on Reddits r/IWantOut subreddit posts and correlates them with World Bank GDP data.

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/migration-analysis-app.git
cd migration-analysis-app
```

2. Create a `.env` file with your Reddit API credentials:
```
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USER_AGENT=migration_analysis_bot
```

3. Install requirements:
```bash
pip install -r requirements.txt
```

4. Run the app:
```bash
streamlit run app.py
```

## Deployment to Streamlit Cloud

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Add your environment variables in Streamlit Cloud settings

## Features

- Analyzes recent posts from r/IWantOut
- Extracts source and destination countries
- Correlates migration patterns with GDP data
- Interactive visualizations
- Data export capabilities

## License

MIT License
```
