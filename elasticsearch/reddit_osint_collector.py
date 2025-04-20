import praw
from elasticsearch import Elasticsearch, helpers
from transformers import pipeline
from langdetect import detect
from datetime import datetime

# إعدادات Reddit API
reddit = praw.Reddit(
    client_id='YOUR_CLIENT_ID',
    client_secret='YOUR_CLIENT_SECRET',
    user_agent='rahhal-osint-agent'
)

# Elasticsearch
es = Elasticsearch("http://localhost:9200")
index_name = "reddit_osint"

# نماذج تحليل المشاعر
sentiment_ar = pipeline("text-classification", model="CAMeL-Lab/bert-base-arabic-camelbert-mix-sentiment")
sentiment_en = pipeline("sentiment-analysis")

def analyze_sentiment(text):
    lang = detect(text)
    if lang == 'ar':
        return sentiment_ar(text)[0]['label']
    else:
        return sentiment_en(text)[0]['label']

# قائمة Subreddits للمتابعة
subreddits = ['UAE', 'AskMiddleEast', 'MiddleEastPeace', 'PublicFreakout', 'Crime']

docs = []
for sub in subreddits:
    subreddit = reddit.subreddit(sub)
    for post in subreddit.new(limit=25):
        if not post.selftext:
            continue
        sentiment = analyze_sentiment(post.selftext)
        doc = {
            "_index": index_name,
            "_source": {
                "subreddit": sub,
                "title": post.title,
                "text": post.selftext,
                "sentiment": sentiment,
                "@timestamp": datetime.utcfromtimestamp(post.created_utc).isoformat()
            }
        }
        docs.append(doc)

# إدخال إلى Elasticsearch
if docs:
    helpers.bulk(es, docs)
    print(f"تم إدخال {len(docs)} مشاركة من Reddit إلى Elasticsearch.")
else:
    print("لا توجد مشاركات متاحة.")
