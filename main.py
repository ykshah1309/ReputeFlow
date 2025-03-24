import pandas as pd
import os
from plugins.reddit_collector import RedditMonitor
from plugins.preprocessing import preprocess_reddit_text
from plugins.modeling import SentimentAnalyzer, TopicModeler
from plugins.alerts import AlertSystem

# Create data directory if missing
os.makedirs("data", exist_ok=True)

def analyze_brand(brand_name, subreddits):
    monitor = RedditMonitor()
    raw_df = monitor.fetch_posts(brand_name, subreddits)
    
    if raw_df.empty:
        return pd.DataFrame(), []
    
    # Preprocessing
    raw_df['clean_text'] = raw_df['title'] + " " + raw_df['content']
    raw_df['clean_text'] = raw_df['clean_text'].apply(preprocess_reddit_text)
    
    # Sentiment Analysis
    analyzer = SentimentAnalyzer()
    raw_df['sentiment'] = analyzer.analyze_batch(raw_df['clean_text'].tolist())
    
    # Topic Modeling
    modeler = TopicModeler()
    modeler.train(raw_df['clean_text'].tolist())
    topics = modeler.get_topics_formatted()
    
    # Save Results
    raw_df.to_csv(f"data/{brand_name}_analysis.csv", index=False)
    
    # Alert System
    alert_checker = AlertSystem()
    negative_pct = (raw_df['sentiment'] == 'NEGATIVE').mean()
    if negative_pct > 0.3:
        alert_checker.send_email(
            f"Negative Sentiment Alert for {brand_name}",
            f"{negative_pct:.1%} negative sentiment detected in recent Reddit posts"
        )
    
    return raw_df, topics