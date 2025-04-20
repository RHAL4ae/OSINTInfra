from elasticsearch import Elasticsearch, helpers
import os
from datetime import datetime

es = Elasticsearch("http://localhost:9200")

docs = []
for file in os.listdir("processing/instagram"):
    if file.endswith(".txt"):
        with open(f"processing/instagram/{file}", "r", encoding="utf-8") as f:
            text = f.read()
        docs.append({
            "_index": "instagram_osint",
            "_source": {
                "filename": file,
                "content": text,
                "@timestamp": datetime.utcnow().isoformat()
            }
        })

helpers.bulk(es, docs)
print("تم إدخال بيانات Instagram إلى Elasticsearch.")
