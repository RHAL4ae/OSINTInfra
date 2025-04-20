<template>
  <div class="dashboard">
    <h2>لوحة بيانات رحّال</h2>

    <div class="kpis">
      <div class="kpi">
        <h3>إجمالي المنشورات</h3>
        <p>{{ totalPosts }}</p>
      </div>
      <div class="kpi">
        <h3>عدد التنبيهات</h3>
        <p>{{ totalAlerts }}</p>
      </div>
      <div class="kpi">
        <h3>نسبة المشاعر السلبية</h3>
        <p>{{ negativePercentage }}%</p>
      </div>
    </div>

    <div class="shortcuts">
      <router-link to="/facebook" class="link">Facebook</router-link>
      <router-link to="/telegram" class="link">Telegram</router-link>
      <router-link to="/twitter" class="link">Twitter</router-link>
      <router-link to="/youtube" class="link">YouTube</router-link>
      <router-link to="/reddit" class="link">Reddit</router-link>
      <router-link to="/linkedin" class="link">LinkedIn</router-link>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Dashboard',
  data() {
    return {
      totalPosts: 0,
      totalAlerts: 0,
      negativePercentage: 0
    }
  },
  async mounted() {
    const indices = ['facebook_osint', 'telegram_osint', 'twitter_osint', 'youtube_osint', 'reddit_osint', 'linkedin_osint']
    let total = 0
    let negative = 0

    for (const index of indices) {
      const res = await axios.post(`http://localhost:9200/${index}/_search`, {
        size: 0,
        aggs: {
          negative_count: {
            filter: { term: { "sentiment.keyword": "negative" } }
          }
        }
      })
      total += res.data.hits.total.value
      negative += res.data.aggregations.negative_count.doc_count
    }

    const alertRes = await axios.get('http://localhost:9200/alert_log/_count')
    this.totalAlerts = alertRes.data.count
    this.totalPosts = total
    this.negativePercentage = total > 0 ? ((negative / total) * 100).toFixed(1) : 0
  }
}
</script>

<style scoped>
.dashboard {
  padding: 2rem;
  font-family: "Cairo", sans-serif;
  direction: rtl;
}
.kpis {
  display: flex;
  gap: 2rem;
  margin-bottom: 2rem;
}
.kpi {
  background: #f0f0f0;
  padding: 1rem 2rem;
  border-radius: 8px;
  flex: 1;
  text-align: center;
}
.kpi h3 {
  margin-bottom: 0.5rem;
}
.shortcuts {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}
.link {
  padding: 0.75rem 1.5rem;
  background: #ddd;
  border-radius: 6px;
  text-decoration: none;
  color: black;
  font-weight: bold;
}
</style>
