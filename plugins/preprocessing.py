import re
import emoji
import spacy
from spacy.lang.en.stop_words import STOP_WORDS

nlp = spacy.load("en_core_web_sm")

def preprocess_reddit_text(text):
    # Remove code blocks and special formatting
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    text = re.sub(r'`.*?`', '', text)
    
    # Convert emojis to text
    text = emoji.demojize(text).replace(":", " ")
    
    # Remove Reddit-specific patterns
    text = re.sub(r'\b\/?r\/\w+\b', '', text)  # Subreddit mentions
    text = re.sub(r'\b\/?u\/\w+\b', '', text)  # User mentions
    text = re.sub(r'^&gt;.*$', '', text, flags=re.MULTILINE)  # Quotes
    
    # Standard cleaning
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    doc = nlp(text.lower())
    
    # Advanced lemmatization with POS filtering
    tokens = [token.lemma_ for token in doc 
              if not token.is_stop 
              and not token.is_punct
              and token.pos_ in ['NOUN', 'ADJ', 'VERB', 'ADV']]
    
    return " ".join(tokens).strip()