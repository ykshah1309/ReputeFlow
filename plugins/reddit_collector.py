import praw
import os
import pandas as pd
from dotenv import load_dotenv
from tqdm import tqdm
import re

load_dotenv()

class RedditMonitor:
    def __init__(self):
        self.reddit = praw.Reddit(
            client_id=os.getenv("REDDIT_CLIENT_ID"),
            client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
            user_agent=os.getenv("REDDIT_USER_AGENT")
        )
    
    def _clean_brand_name(self, brand_name):
        """Sanitize brand name for search"""
        return re.sub(r'[^\w\s-]', '', brand_name).strip()
    
    def fetch_posts(self, brand_name, subreddits, limit=100):
        brand_name = self._clean_brand_name(brand_name)
        posts = []
        subreddits_str = "+".join(subreddits)
        
        try:
            # Improved search query with case-insensitive variants
            query = f"{brand_name} OR {brand_name.lower()} OR {brand_name.upper()}"
            
            for submission in tqdm(self.reddit.subreddit(subreddits_str).search(
                query=query,
                sort="new",
                time_filter="month",
                limit=limit
            ), desc=f"Fetching posts about {brand_name}"):
                posts.append({
                    "brand": brand_name,
                    "title": submission.title,
                    "content": submission.selftext,
                    "author": str(submission.author),
                    "subreddit": submission.subreddit.display_name,
                    "created_utc": submission.created_utc,
                    "url": f"https://reddit.com{submission.permalink}",
                    "score": submission.score
                })
        except Exception as e:
            print(f"Error fetching data: {e}")
        
        return pd.DataFrame(posts)