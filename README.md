```markdown
# Migration Pattern Analysis App

This Streamlit app analyzes migration patterns based on Reddit's r/IWantOut subreddit posts and correlates them with World Bank GDP data.

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
