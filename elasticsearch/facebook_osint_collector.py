import requests
from datetime import datetime, timedelta
from transformers import pipeline
from langdetect import detect
from elasticsearch import Elasticsearch, helpers

# إعدادات Facebook
ACCESS_TOKEN = 'YOUR_ACCESS_TOKEN_HERE'
PAGE_ID = 'YOUR_PAGE_ID_HERE'
DAYS_BACK = 7

# إعدادات Elasticsearch
es = Elasticsearch("http://localhost:9200")
index_name = "facebook_osint"

# تحميل نماذج تحليل المشاعر
sentiment_ar = pipeline("text-classification", model="CAMeL-Lab/bert-base-arabic-camelbert-mix-sentiment")
sentiment_en = pipeline("sentiment-analysis")

# دالة تحليل النص
def analyze_text(text):
    lang = detect(text)
    if lang == "ar":
        sentiment = sentiment_ar(text)[0]['label']
    else:
        sentiment = sentiment_en(text)[0]['label']
    return sentiment

# وقت البدء
since_date = (datetime.utcnow() - timedelta(days=DAYS_BACK)).isoformat()

# API طلب المنشورات
url = f"https://graph.facebook.com/v18.0/{PAGE_ID}/posts"
params = {
    'access_token': ACCESS_TOKEN,
    'fields': 'message,created_time,id',
    'since': since_date
}

# تنفيذ الطلب
response = requests.get(url, params=params)
data = response.json()

# تجهيز البيانات لـ Elasticsearch
docs = []
for post in data.get('data', []):
    text = post.get('message', '')
    if not text:
        continue

    sentiment = analyze_text(text)
    doc = {
        "_index": index_name,
        "_source": {
            "content": text,
            "sentiment": sentiment,
            "@timestamp": post.get('created_time')
        }
    }
    docs.append(doc)

# إدخال إلى Elasticsearch
if docs:
    helpers.bulk(es, docs)
    print(f"تم إدخال {len(docs)} منشور إلى Elasticsearch.")
else:
    print("لا توجد منشورات متاحة أو محتوى فارغ.")
