<template>
  <div class="reddit-feed">
    <h2>رصد مشاركات Reddit</h2>

    <div class="filters">
      <label>تصفية حسب المشاعر:</label>
      <select v-model="selectedSentiment" @change="fetchPosts">
        <option value="">الكل</option>
        <option value="positive">إيجابي</option>
        <option value="negative">سلبي</option>
        <option value="neutral">محايد</option>
      </select>

      <label>Subreddit:</label>
      <select v-model="selectedSubreddit" @change="fetchPosts">
        <option value="">الكل</option>
        <option v-for="s in subreddits" :key="s" :value="s">{{ s }}</option>
      </select>
    </div>

    <table>
      <thead>
        <tr>
          <th>Subreddit</th>
          <th>العنوان</th>
          <th>النص</th>
          <th>المشاعر</th>
          <th>التاريخ</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="post in posts" :key="post._id">
          <td>{{ post._source.subreddit }}</td>
          <td>{{ post._source.title }}</td>
          <td>{{ post._source.text }}</td>
          <td>{{ post._source.sentiment }}</td>
          <td>{{ post._source['@timestamp'] }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'RedditFeed',
  data() {
    return {
      posts: [],
      subreddits: [],
      selectedSentiment: '',
      selectedSubreddit: ''
    }
  },
  async mounted() {
    await this.fetchPosts()
  },
  methods: {
    async fetchPosts() {
      const filters = []

      if (this.selectedSentiment) {
        filters.push({ term: { "sentiment.keyword": this.selectedSentiment } })
      }
      if (this.selectedSubreddit) {
        filters.push({ term: { "subreddit.keyword": this.selectedSubreddit } })
      }

      const query = {
        size: 50,
        sort: [{ "@timestamp": { order: "desc" } }],
        query: filters.length > 0 ? { bool: { must: filters } } : { match_all: {} }
      }

      const res = await axios.post('http://localhost:9200/reddit_osint/_search', query)
      this.posts = res.data.hits.hits

      // استخرج جميع subreddits المتوفرة بشكل ديناميكي
      const allSubs = [...new Set(this.posts.map(p => p._source.subreddit))].sort()
      this.subreddits = allSubs
    }
  }
}
</script>

<style scoped>
.reddit-feed {
  padding: 2rem;
  direction: rtl;
  font-family: "Cairo", sans-serif;
}
.filters {
  margin-bottom: 1rem;
  display: flex;
  gap: 2rem;
  align-items: center;
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
