from transformers import pipeline
from gensim import corpora, models
import os

class SentimentAnalyzer:
    def __init__(self):
        self.classifier = pipeline(
            "sentiment-analysis",
            model="cardiffnlp/twitter-roberta-base-sentiment",
            return_all_scores=True
        )
        self.label_map = {
            "LABEL_0": "NEGATIVE",
            "LABEL_1": "NEUTRAL",
            "LABEL_2": "POSITIVE"
        }

    def analyze_batch(self, texts):
        results = []
        for text in texts:
            if len(text) > 512:
                text = text[:512]
            try:
                scores = self.classifier(text)[0]
                best = max(scores, key=lambda x: x['score'])
                results.append(self.label_map[best['label']])
            except Exception as e:
                print(f"Error analyzing text: {e}")
                results.append("NEUTRAL")
        return results

class TopicModeler:
    def __init__(self, num_topics=4):
        self.lda_model = None
        self.dictionary = None
        self.num_topics = num_topics

    def train(self, texts):
        tokenized = [text.split() for text in texts]
        self.dictionary = corpora.Dictionary(tokenized)
        corpus = [self.dictionary.doc2bow(text) for text in tokenized]
        self.lda_model = models.LdaModel(
            corpus,
            num_topics=self.num_topics,
            id2word=self.dictionary,
            passes=15,
            alpha='auto'
        )

    def get_topics_formatted(self):
        topics = []
        for idx, topic in self.lda_model.print_topics(-1):
            topic_words = [word.split("*")[1].strip('"') for word in topic.split("+")]
            topics.append(", ".join(topic_words[:5]))
        return topics