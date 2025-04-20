<template>
  <div class="linkedin-feed">
    <h2>رصد منشورات LinkedIn</h2>
    <table>
      <thead>
        <tr>
          <th>المصدر</th>
          <th>المحتوى</th>
          <th>المشاعر</th>
          <th>الوقت</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="post in posts" :key="post._id">
          <td>{{ post._source.source }}</td>
          <td>{{ post._source.content }}</td>
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
  name: 'LinkedInFeed',
  data() {
    return {
      posts: []
    }
  },
  mounted() {
    axios.get('http://localhost:9200/linkedin_osint/_search?size=50&sort=@timestamp:desc')
      .then(res => {
        this.posts = res.data.hits.hits
      })
  }
}
</script>

<style scoped>
.linkedin-feed {
  padding: 2rem;
  direction: rtl;
  font-family: "Cairo", sans-serif;
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
