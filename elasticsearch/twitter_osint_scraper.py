import snscrape.modules.twitter as sntwitter
from transformers import pipeline
from langdetect import detect
from elasticsearch import Elasticsearch, helpers
from datetime import datetime

# إعدادات البحث
query = "#عجمان OR شرطة عجمان"
max_results = 100

# Elasticsearch
es = Elasticsearch("http://localhost:9200")
index_name = "twitter_osint"

# نماذج تحليل المشاعر
sentiment_ar = pipeline("text-classification", model="CAMeL-Lab/bert-base-arabic-camelbert-mix-sentiment")
sentiment_en = pipeline("sentiment-analysis")

def analyze_sentiment(text):
    lang = detect(text)
    if lang == 'ar':
        return sentiment_ar(text)[0]['label']
    else:
        return sentiment_en(text)[0]['label']

# جمع البيانات
docs = []
for tweet in sntwitter.TwitterSearchScraper(query).get_items():
    if len(docs) >= max_results:
        break

    text = tweet.content
    sentiment = analyze_sentiment(text)
    doc = {
        "_index": index_name,
        "_source": {
            "username": tweet.user.username,
            "content": text,
            "sentiment": sentiment,
            "@timestamp": tweet.date.isoformat()
        }
    }
    docs.append(doc)

# إدخال النتائج
if docs:
    helpers.bulk(es, docs)
    print(f"تم إدخال {len(docs)} تغريدة.")
else:
    print("لا توجد تغريدات.")
