from elasticsearch import Elasticsearch, helpers
import os
from datetime import datetime

es = Elasticsearch("http://localhost:9200")

docs = []
for file in os.listdir("processing/tiktok"):
    if file.endswith(".txt"):
        with open(f"processing/tiktok/{file}", "r", encoding="utf-8") as f:
            text = f.read()
        docs.append({
            "_index": "tiktok_osint",
            "_source": {
                "filename": file,
                "content": text,
                "@timestamp": datetime.utcnow().isoformat()
            }
        })

helpers.bulk(es, docs)
print("تم إدخال بيانات TikTok إلى Elasticsearch.")
