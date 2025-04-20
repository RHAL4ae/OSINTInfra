<template>
  <div class="fb-feed">
    <h2>رصد منشورات Facebook</h2>

    <div class="filters">
      <label>تصفية حسب الوقت:</label>
      <select v-model="selectedTimeRange" @change="loadPosts">
        <option value="">كل الأوقات</option>
        <option value="now-1d/d">آخر 24 ساعة</option>
        <option value="now-7d/d">آخر 7 أيام</option>
        <option value="now-30d/d">آخر 30 يوم</option>
      </select>
    </div>

    <form @submit.prevent="submitPost" class="new-post-form">
      <textarea v-model="newContent" placeholder="أدخل منشورًا جديدًا..." required></textarea>
      <button type="submit">تحليل وإدخال</button>
    </form>

    <table>
      <thead>
        <tr>
          <th>الوقت</th>
          <th>النص</th>
          <th>المشاعر</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="post in posts" :key="post._id">
          <td>{{ post._source['@timestamp'] }}</td>
          <td>{{ post._source.content }}</td>
          <td>{{ post._source.sentiment }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'FacebookFeed',
  data() {
    return {
      posts: [],
      newContent: '',
      selectedTimeRange: ''
    }
  },
  mounted() {
    this.loadPosts()
  },
  methods: {
    async loadPosts() {
      const res = await axios.post('http://localhost:9200/facebook_osint/_search', {
        size: 50,
        sort: [{ "@timestamp": { order: "desc" } }],
        query: this.selectedTimeRange ? {
          range: {
            "@timestamp": {
              gte: this.selectedTimeRange
            }
          }
        } : { match_all: {} }
      })
      this.posts = res.data.hits.hits
    },
    async submitPost() {
      if (!this.newContent.trim()) return

      // تحليل المشاعر
      const detectLang = await axios.post('https://libretranslate.de/detect', { q: this.newContent })
      const lang = detectLang.data[0].language

      let sentiment = 'neutral'
      if (lang === 'ar') {
        const res = await axios.post('https://api-inference.huggingface.co/models/CAMeL-Lab/bert-base-arabic-camelbert-mix-sentiment', {
          inputs: this.newContent
        })
        sentiment = res.data[0]?.label || 'neutral'
      } else {
        const res = await axios.post('https://api-inference.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2-english', {
          inputs: this.newContent
        })
        sentiment = res.data[0]?.label || 'neutral'
      }

      // إدخال إلى Elasticsearch
      await axios.post('http://localhost:9200/facebook_osint/_doc', {
        content: this.newContent,
        sentiment: sentiment,
        '@timestamp': new Date().toISOString()
      })

            // تحقق من المخاطر
      const highRiskKeywords = ['قتل', 'انفجار', 'تفجير', 'سلاح', 'تهديد']
      const isHighRisk = highRiskKeywords.some(k => this.newContent.includes(k)) || sentiment.toLowerCase() === 'negative'

      // إرسال تنبيه إذا وجد خطر
      if (isHighRisk) {
        await axios.post('http://localhost:9200/alert_log/_doc', {
          time: new Date().toISOString(),
          alert_type: "facebook_manual_entry",
          source: "manual_form",
          sentiment: sentiment,
          content: this.newContent
        })
      }

      this.newContent = ''
      this.loadPosts()
    }
  }
}
</script>

<style scoped>
.fb-feed {
  padding: 2rem;
  direction: rtl;
  font-family: "Cairo", sans-serif;
}
.new-post-form {
  margin-bottom: 2rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
textarea {
  width: 100%;
  height: 100px;
  padding: 1rem;
  font-size: 1rem;
  font-family: "Cairo", sans-serif;
}
button {
  width: 200px;
  padding: 0.75rem;
  font-weight: bold;
  cursor: pointer;
  align-self: flex-start;
}
table {
  width: 100%;
  border-collapse: collapse;
}
th, td {
  border: 1px solid #ccc;
  padding: 0.75rem;
  text-align: right;
}
</style>
