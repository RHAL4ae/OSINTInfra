from elasticsearch import Elasticsearch, helpers
import os

es = Elasticsearch("http://localhost:9200")

docs = []
for file in os.listdir("processing"):
    if file.endswith(".txt"):
        with open(f"processing/{file}", "r", encoding="utf-8") as f:
            text = f.read()
        docs.append({
            "_index": "snapchat_osint",
            "_source": {
                "filename": file,
                "content": text
            }
        })

helpers.bulk(es, docs)
print("تم إدخال النصوص إلى Elasticsearch بنجاح.")
