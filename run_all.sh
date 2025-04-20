#!/bin/bash

echo "1. تشغيل Docker..."
docker-compose -f docker-compose.yml up -d

echo "2. تفعيل البيئة..."
sleep 15  # انتظر Elasticsearch و Kibana لتشتغل

echo "3. تنفيذ سكربت Whisper لتحويل الفيديوهات إلى نص..."
python3 processing/whisper_transcribe.py

echo "4. إدخال البيانات إلى Elasticsearch..."
python3 elasticsearch/ingest_to_es_with_timestamp.py

echo "5. تم تنفيذ جميع الخطوات بنجاح. ادخل إلى Kibana على: http://localhost:5601"
