import requests
from googleapiclient.discovery import build
from transformers import pipeline
from langdetect import detect
from elasticsearch import Elasticsearch, helpers
from datetime import datetime

# إعدادات API
API_KEY = 'YOUR_YOUTUBE_API_KEY'
YOUTUBE = build('youtube', 'v3', developerKey=API_KEY)
QUERY = 'الشرطة في عجمان'
MAX_RESULTS = 5

# Elasticsearch
es = Elasticsearch("http://localhost:9200")
index_name = "youtube_osint"

# تحليل المشاعر
sentiment_ar = pipeline("text-classification", model="CAMeL-Lab/bert-base-arabic-camelbert-mix-sentiment")
sentiment_en = pipeline("sentiment-analysis")

def analyze_sentiment(text):
    lang = detect(text)
    if lang == 'ar':
        return sentiment_ar(text)[0]['label']
    else:
        return sentiment_en(text)[0]['label']

# البحث عن الفيديوهات
search_response = YOUTUBE.search().list(
    q=QUERY,
    type='video',
    part='id,snippet',
    maxResults=MAX_RESULTS
).execute()

docs = []

# لكل فيديو نجلب التعليقات
for item in search_response.get('items', []):
    video_id = item['id']['videoId']
    title = item['snippet']['title']
    published = item['snippet']['publishedAt']

    comments_response = YOUTUBE.commentThreads().list(
        part='snippet',
        videoId=video_id,
        maxResults=20,
        textFormat='plainText'
    ).execute()

    for comment_item in comments_response.get('items', []):
        comment = comment_item['snippet']['topLevelComment']['snippet']
        text = comment['textDisplay']
        time = comment['publishedAt']
        sentiment = analyze_sentiment(text)

        doc = {
            "_index": index_name,
            "_source": {
                "video_title": title,
                "video_id": video_id,
                "comment": text,
                "sentiment": sentiment,
                "@timestamp": time
            }
        }
        docs.append(doc)

# إدخال البيانات
helpers.bulk(es, docs)
print(f"تم إدخال {len(docs)} تعليقًا إلى Elasticsearch.")
