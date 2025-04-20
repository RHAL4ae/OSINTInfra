import os
import whisper
from transformers import pipeline
from langdetect import detect
from datetime import datetime
from elasticsearch import Elasticsearch, helpers

# تحميل النماذج
sentiment_ar = pipeline("text-classification", model="CAMeL-Lab/bert-base-arabic-camelbert-mix-sentiment")
sentiment_en = pipeline("sentiment-analysis")

# تصنيف النية والمخاطر (مبسط)
def classify_context(text):
    keywords = {
        "تحذير": "warning",
        "تهديد": "threat",
        "نجدة": "distress",
        "حريق": "high",
        "انفجار": "high",
        "بلاغ": "report",
        "قتل": "high",
        "سيء": "medium",
        "كلب": "low",
    }
    for k, v in keywords.items():
        if k in text:
            return v
    return "neutral"

def analyze_text(text):
    lang = detect(text)
    if lang == "ar":
        sentiment = sentiment_ar(text)[0]['label']
    else:
        sentiment = sentiment_en(text)[0]['label']
    risk = classify_context(text)
    return sentiment, risk

# Whisper لتحويل الصوت
model = whisper.load_model("base")

input_dir = "downloads/instagram"
output_dir = "processing/instagram"
os.makedirs(output_dir, exist_ok=True)

# Elasticsearch
es = Elasticsearch("http://localhost:9200")
docs = []

# المعالجة الكاملة
for file in os.listdir(input_dir):
    if file.endswith(".mp4"):
        audio_path = os.path.join(input_dir, file)
        print(f"تحويل: {audio_path}")
        result = model.transcribe(audio_path)
        text = result['text']

        # تصنيف
        sentiment, risk = analyze_text(text)

        # حفظ الملف نصي
        with open(os.path.join(output_dir, f"{file}.txt"), "w", encoding='utf-8') as out_file:
            out_file.write(text)

        # إرسال لـ Elasticsearch
        docs.append({
            "_index": "instagram_osint",
            "_source": {
                "filename": file,
                "content": text,
                "sentiment": sentiment,
                "risk_level": risk,
                "@timestamp": datetime.utcnow().isoformat()
            }
        })

helpers.bulk(es, docs)
print("تم تحليل وإدخال فيديوهات Instagram مع التصنيفات.")
