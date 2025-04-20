# مشروع رحّال | RAHHAL OSINT Intelligence Platform

منصة رحّال هي منصة سيادية ذكية لرصد وتحليل المحتوى المفتوح (OSINT) باستخدام الذكاء الاصطناعي، مصممة لدعم الجهات الأمنية والحكومية في العالم العربي.

---

## الميزات الرئيسية:
- جمع وتحليل المحتوى من منصات: Twitter, Facebook, Telegram, YouTube, Reddit, LinkedIn
- تحليل مشاعر ونصوص باللغتين العربية والإنجليزية
- تصنيف تلقائي للمخاطر (مرتفع، متوسط، منخفض)
- دعم كامل للغة العربية والوضع الليلي (Dark Mode)
- واجهة Vue.js متكاملة + Kibana Dashboard
- تنبيهات فورية عبر Watcher
- خرائط تفاعلية وتحليل زمني متقدم
- تصميم متوافق مع الهوية الرسمية لـ AEGov

---

## بنية المشروع

```bash
rahhal/
├── frontend/              # واجهة المستخدم (Vue 3)
│   └── src/views/         # صفحات التحليل لكل منصة (FacebookFeed.vue, TwitterFeed.vue, ...)
├── elasticsearch/         # سكربتات جمع وتحليل البيانات (telegram_osint_collector.py, ...)
├── backend/               # API وواجهات FastAPI (إن وجدت)
├── docker-compose.yml     # تهيئة الحاويات (Elasticsearch, Kibana)
├── Dashboard.vue          # لوحة البيانات الموحدة
├── main.css               # تخصيص التصميم والهوية البصرية
├── requirements.txt       # الحزم اللازمة للتشغيل
├── Rahhal_Executive_Presentation_Arabic.pptx   # عرض تنفيذي
├── Rahhal_Full_Technical_SOP_Integrated.docx   # مستند تقني رسمي
└── README.md              # هذا الملف
```

---

## خطوات التشغيل

```bash
# 1. تثبيت الحزم
pip install -r requirements.txt

# 2. تشغيل الحاويات
docker-compose up -d

# 3. تشغيل الواجهة
cd frontend
npm install
npm run dev
```

---

## الاستخدامات المستهدفة

- الجهات الأمنية والشرطية
- مراكز الإعلام والتحقق الرقمي
- البلديات والهيئات الحكومية
- مراكز تحليل الرأي العام

---

## التراخيص
النسخة الحالية للعرض التجريبي والتقييم فقط. جميع الحقوق محفوظة لمؤسس المشروع.

"# OSINTInfra" 
