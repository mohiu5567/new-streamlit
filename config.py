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
