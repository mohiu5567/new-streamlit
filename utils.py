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
