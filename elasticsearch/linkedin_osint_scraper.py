from requests_html import HTMLSession
from transformers import pipeline
from langdetect import detect
from elasticsearch import Elasticsearch, helpers
from datetime import datetime

# إعدادات
url = "https://www.linkedin.com/company/dubaipolice"
es = Elasticsearch("http://localhost:9200")
index_name = "linkedin_osint"

# تحميل نماذج المشاعر
sentiment_ar = pipeline("text-classification", model="CAMeL-Lab/bert-base-arabic-camelbert-mix-sentiment")
sentiment_en = pipeline("sentiment-analysis")

def analyze_sentiment(text):
    lang = detect(text)
    return sentiment_ar(text)[0]['label'] if lang == 'ar' else sentiment_en(text)[0]['label']

# بدء جلسة
session = HTMLSession()
r = session.get(url)
r.html.render(timeout=20)

# استخراج النصوص العامة (غير مضمونة 100%)
elements = r.html.find("span.break-words", first=False)

docs = []
for e in elements:
    text = e.text.strip()
    if len(text) < 20:
        continue
    sentiment = analyze_sentiment(text)
    docs.append({
        "_index": index_name,
        "_source": {
            "source": "linkedin.com/company/dubaipolice",
            "content": text,
            "sentiment": sentiment,
            "@timestamp": datetime.utcnow().isoformat()
        }
    })

# إدخال إلى Elasticsearch
if docs:
    helpers.bulk(es, docs)
    print(f"تم إدخال {len(docs)} منشور من LinkedIn.")
else:
    print("لم يتم العثور على محتوى كافٍ.")

session.close()
