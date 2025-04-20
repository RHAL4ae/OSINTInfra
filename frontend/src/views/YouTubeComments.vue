<template>
  <div class="youtube-comments">
    <h2>تحليل تعليقات YouTube</h2>

    <div class="filters">
      <label>تصفية حسب الوقت:</label>
      <select v-model="selectedTimeRange" @change="fetchComments">
        <option value="">كل الأوقات</option>
        <option value="now-1d/d">آخر 24 ساعة</option>
        <option value="now-7d/d">آخر 7 أيام</option>
        <option value="now-30d/d">آخر 30 يوم</option>
      </select>
  </div>
  <div class="filters">
      <label>تصفية حسب المشاعر:</label>
      <select v-model="selectedSentiment" @change="fetchComments">
        <option value="">الكل</option>
        <option value="positive">إيجابي</option>
        <option value="negative">سلبي</option>
        <option value="neutral">محايد</option>
      </select>
    </div>

    <table>
      <thead>
        <tr>
          <th>الفيديو</th>
          <th>التعليق</th>
          <th>المشاعر</th>
          <th>التاريخ</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="comment in comments" :key="comment._id">
          <td>{{ comment._source.video_title }}</td>
          <td>{{ comment._source.comment }}</td>
          <td>{{ comment._source.sentiment }}</td>
          <td>{{ comment._source['@timestamp'] }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'YouTubeComments',
  data() {
    return {
      comments: [],
      selectedSentiment: '',
      selectedTimeRange: ''
    }
  },
  mounted() {
    this.fetchComments()
  },
  methods: {
    async fetchComments() {
      const query = {
        size: 50,
        sort: [{ "@timestamp": { "order": "desc" } }],
        query: {
        bool: {
          must: [
            this.selectedSentiment ? { term: { "sentiment.keyword": this.selectedSentiment } } : { match_all: {} },
            this.selectedTimeRange ? { range: { "@timestamp": { gte: this.selectedTimeRange } } } : { match_all: {} }
          ]
        }
      }
          ? { term: { "sentiment.keyword": this.selectedSentiment } }
          : { match_all: {} }
      }

      const res = await axios.post('http://localhost:9200/youtube_osint/_search', query)
      this.comments = res.data.hits.hits
    }
  }
}
</script>

<style scoped>
.youtube-comments {
  padding: 2rem;
  direction: rtl;
  font-family: "Cairo", sans-serif;
}
.filters {
  margin-bottom: 1rem;
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
