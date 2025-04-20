<template>
  <div class="twitter-feed">
    <h2>تحليل تغريدات Twitter</h2>

    <div class="filters">
      <label>المشاعر:</label>
      <select v-model="selectedSentiment" @change="fetchTweets">
        <option value="">الكل</option>
        <option value="positive">إيجابي</option>
        <option value="negative">سلبي</option>
        <option value="neutral">محايد</option>
      </select>

      <label>المستخدم:</label>
      <select v-model="selectedUser" @change="fetchTweets">
        <option value="">الكل</option>
        <option v-for="u in users" :key="u" :value="u">{{ u }}</option>
      </select>

      <label>الفترة:</label>
      <select v-model="selectedTimeRange" @change="fetchTweets">
        <option value="">كل الأوقات</option>
        <option value="now-1d/d">آخر 24 ساعة</option>
        <option value="now-7d/d">آخر 7 أيام</option>
        <option value="now-30d/d">آخر 30 يوم</option>
      </select>
    </div>

    <table>
      <thead>
        <tr>
          <th>المستخدم</th>
          <th>التغريدة</th>
          <th>المشاعر</th>
          <th>التاريخ</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="tweet in tweets" :key="tweet._id">
          <td>{{ tweet._source.username }}</td>
          <td>{{ tweet._source.content }}</td>
          <td>{{ tweet._source.sentiment }}</td>
          <td>{{ tweet._source['@timestamp'] }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'TwitterFeed',
  data() {
    return {
      tweets: [],
      users: [],
      selectedSentiment: '',
      selectedUser: '',
      selectedTimeRange: ''
    }
  },
  mounted() {
    this.fetchTweets()
  },
  methods: {
    async fetchTweets() {
      const filters = []

      if (this.selectedSentiment)
        filters.push({ term: { "sentiment.keyword": this.selectedSentiment } })

      if (this.selectedUser)
        filters.push({ term: { "username.keyword": this.selectedUser } })

      if (this.selectedTimeRange)
        filters.push({ range: { "@timestamp": { gte: this.selectedTimeRange } } })

      const query = {
        size: 50,
        sort: [{ "@timestamp": { order: "desc" } }],
        query: filters.length > 0 ? { bool: { must: filters } } : { match_all: {} }
      }

      const res = await axios.post('http://localhost:9200/twitter_osint/_search', query)
      this.tweets = res.data.hits.hits
      this.users = [...new Set(this.tweets.map(t => t._source.username))].sort()
    }
  }
}
</script>

<style scoped>
.twitter-feed {
  padding: 2rem;
  direction: rtl;
  font-family: "Cairo", sans-serif;
}
.filters {
  margin-bottom: 1rem;
  display: flex;
  gap: 1.5rem;
  align-items: center;
  flex-wrap: wrap;
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
