<template>
  <div class="alerts-container">
    <h2>تنبيهات المخاطر والمشاعر السلبية</h2>

    <div class="filters">
      <label>تصفية حسب الوقت:</label>
      <select v-model="selectedTimeRange" @change="fetchAlerts">
        <option value="">كل الأوقات</option>
        <option value="now-1d/d">آخر 24 ساعة</option>
        <option value="now-7d/d">آخر 7 أيام</option>
        <option value="now-30d/d">آخر 30 يوم</option>
      </select>
    </div>

    <table>
      <thead>
        <tr>
          <th>الوقت</th>
          <th>النوع</th>
          <th>عدد النتائج</th>
          <th>المحتوى</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="alert in alerts" :key="alert.time">
          <td>{{ alert.time }}</td>
          <td>{{ alert.alert_type }}</td>
          <td>{{ JSON.parse(alert.items).length }}</td>
          <td>
            <details>
              <summary>عرض</summary>
              <pre>{{ alert.items }}</pre>
            </details>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Alerts',
  data() {
    return {
      alerts: [],
      selectedTimeRange: ''
    }
  },
  mounted() {
    this.fetchAlerts()
  },
  methods: {
    async fetchAlerts() {
      const query = {
        size: 50,
        sort: [{ "@timestamp": { order: "desc" } }],
        query: this.selectedTimeRange
          ? { range: { "@timestamp": { gte: this.selectedTimeRange } } }
          : { match_all: {} }
      }

      const res = await axios.post('http://localhost:9200/alert_log/_search', query)
      this.alerts = res.data.hits.hits.map(hit => hit._source)
    }
  }
}
</script>

<style scoped>
.alerts-container {
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
td, th {
  border: 1px solid #ccc;
  padding: 0.75rem;
}
</style>
