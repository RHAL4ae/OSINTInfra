from telethon.sync import TelegramClient
from elasticsearch import Elasticsearch, helpers
from transformers import pipeline
from langdetect import detect
from datetime import datetime

# إعدادات Telegram API
api_id = 'YOUR_API_ID'
api_hash = 'YOUR_API_HASH'
channel_username = 'ajmanpolice'  # اسم القناة العامة بدون @

# إنشاء العميل (أول مرة سيطلب كود تسجيل دخول)
client = TelegramClient('rahhal_session', api_id, api_hash)
client.start()

# Elasticsearch
es = Elasticsearch("http://localhost:9200")
index_name = "telegram_osint"

# نماذج المشاعر
sentiment_ar = pipeline("text-classification", model="CAMeL-Lab/bert-base-arabic-camelbert-mix-sentiment")
sentiment_en = pipeline("sentiment-analysis")

def analyze_sentiment(text):
    lang = detect(text)
    if lang == 'ar':
        return sentiment_ar(text)[0]['label']
    else:
        return sentiment_en(text)[0]['label']

# جلب الرسائل
docs = []
for message in client.iter_messages(channel_username, limit=50):
    if not message.text:
        continue

    sentiment = analyze_sentiment(message.text)
    doc = {
        "_index": index_name,
        "_source": {
            "channel": channel_username,
            "message": message.text,
            "sentiment": sentiment,
            "@timestamp": message.date.isoformat()
        }
    }
    docs.append(doc)

# إدخال البيانات
if docs:
    helpers.bulk(es, docs)
    print(f"تم إدخال {len(docs)} رسالة من Telegram.")
else:
    print("لا توجد رسائل نصية.")

client.disconnect()
