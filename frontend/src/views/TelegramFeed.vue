<template>
  <div class="telegram-feed">
    <h2>تحليل رسائل Telegram</h2>

    <div class="filters">
      <label>تصفية حسب المشاعر:</label>
      <select v-model="selectedSentiment" @change="fetchMessages">
        <option value="">الكل</option>
        <option value="positive">إيجابي</option>
        <option value="negative">سلبي</option>
        <option value="neutral">محايد</option>
      </select>

      <label>القناة:</label>
      <select v-model="selectedChannel" @change="fetchMessages">
        <option value="">الكل</option>
        <option v-for="c in channels" :key="c" :value="c">{{ c }}</option>
      </select>

      <label>الفترة:</label>
      <select v-model="selectedTimeRange" @change="fetchMessages">
        <option value="">كل الأوقات</option>
        <option value="now-1d/d">آخر 24 ساعة</option>
        <option value="now-7d/d">آخر 7 أيام</option>
        <option value="now-30d/d">آخر 30 يوم</option>
      </select>
    </div>

    <table>
      <thead>
        <tr>
          <th>القناة</th>
          <th>الرسالة</th>
          <th>المشاعر</th>
          <th>التاريخ</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="msg in messages" :key="msg._id">
          <td>{{ msg._source.channel }}</td>
          <td>{{ msg._source.message }}</td>
          <td>{{ msg._source.sentiment }}</td>
          <td>{{ msg._source['@timestamp'] }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'TelegramFeed',
  data() {
    return {
      messages: [],
      selectedSentiment: '',
      selectedChannel: '',
      selectedTimeRange: '',
      channels: []
    }
  },
  async mounted() {
    await this.fetchMessages()
  },
  methods: {
    async fetchMessages() {
      const filters = []

      if (this.selectedSentiment)
        filters.push({ term: { "sentiment.keyword": this.selectedSentiment } })

      if (this.selectedChannel)
        filters.push({ term: { "channel.keyword": this.selectedChannel } })

      if (this.selectedTimeRange)
        filters.push({ range: { "@timestamp": { gte: this.selectedTimeRange } } })

      const query = {
        size: 50,
        sort: [{ "@timestamp": { order: "desc" } }],
        query: filters.length > 0 ? { bool: { must: filters } } : { match_all: {} }
      }

      const res = await axios.post('http://localhost:9200/telegram_osint/_search', query)
      this.messages = res.data.hits.hits

      // تحديث القنوات المتاحة ديناميكيًا
      this.channels = [...new Set(this.messages.map(m => m._source.channel))].sort()
    }
  }
}
</script>

<style scoped>
.telegram-feed {
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
