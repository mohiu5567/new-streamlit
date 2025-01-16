import praw
import re
from collections import Counter
from fuzzywuzzy import fuzz, process
import wbdata
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Initialize PRAW with your credentials
reddit = praw.Reddit(client_id='YOUR_CLIENT_ID',
                     client_secret='YOUR_CLIENT_SECRET',
                     user_agent='YOUR_USER_AGENT')

# Get recent posts from the subreddit
subreddit = reddit.subreddit('IWantOut')
posts = [post.title for post in subreddit.new(limit=1000)]

# Define regex patterns for country names
country_pattern = re.compile(r'\b(?:USA|Canada|Germany|France|...)\b', re.IGNORECASE)

# Extract countries from post titles
countries = [country_pattern.findall(post) for post in posts]

# Flatten the list of countries and count occurrences
flat_countries = [country for sublist in countries for country in sublist]
country_counts = Counter(flat_countries)

# Handle different spellings using fuzzy matching
unique_countries = list(set(flat_countries))
matched_countries = {country: process.extractOne(country, unique_countries, scorer=fuzz.ratio)[0] for country in unique_countries}

# Get GDP per capita data
gdp_data = wbdata.get_dataframe({'NY.GDP.PCAP.CD': 'GDP per capita'}, convert_date=False)

# Match Reddit country list with GDP data
gdp_countries = gdp_data.index.get_level_values(0).tolist()
matched_gdp = {country: process.extractOne(country, gdp_countries, scorer=fuzz.ratio)[0] for country in unique_countries}

# Create data frame with Reddit mentions and GDP data
data = {
    'Country': unique_countries,
    'Reddit Mentions': [country_counts[country] for country in unique_countries],
    'GDP per Capita': [gdp_data.loc[matched_gdp[country]].values[0] for country in unique_countries]
}
df = pd.DataFrame(data)

# Scatterplot for origin countries
plt.figure(figsize=(10, 6))
plt.scatter(df['GDP per Capita'], df['Reddit Mentions'])
plt.xlabel('GDP per Capita')
plt.ylabel('Reddit Mentions')
plt.title('Origin Countries and GDP')
plt.show()

# Scatterplot for destination countries
plt.figure(figsize=(10, 6))
plt.scatter(df['GDP per Capita'], df['Reddit Mentions'])
plt.xlabel('GDP per Capita')
plt.ylabel('Reddit Mentions')
plt.title('Destination Countries and GDP')
plt.show()

# Streamlit app
st.title('Migration Patterns Based on Reddit Posts')
st.write('This app investigates migration patterns based on Reddit posts from the subreddit "IWantOut".')

st.write('### Data Frame')
st.dataframe(df)

st.write('### Scatterplot for Origin Countries')
st.pyplot(fig1)

st.write('### Scatterplot for Destination Countries')
st.pyplot(fig2)
