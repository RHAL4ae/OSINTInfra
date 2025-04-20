<template>
  <div class="analytics-container">
    <h2>التحليل الذكي للمشاعر والمخاطر</h2>
    <div class="charts">
      <div class="chart">
        <h3>توزيع المشاعر</h3>
        <canvas id="sentimentChart"></canvas>
      </div>
      <div class="chart">
        <h3>تصنيف المخاطر حسب المصدر</h3>
        <canvas id="riskChart"></canvas>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import Chart from 'chart.js/auto'

export default {
  name: 'Analytics',
  data() {
    return {
      sentimentData: { positive: 0, negative: 0, neutral: 0 },
      riskData: {
        snapchat: { high: 0, medium: 0, low: 0 },
        tiktok: { high: 0, medium: 0, low: 0 },
        instagram: { high: 0, medium: 0, low: 0 }
      }
    }
  },
  methods: {
    async fetchData() {
      const sources = ['snapchat_osint', 'tiktok_osint', 'instagram_osint']
      for (let index of sources) {
        const res = await axios.post(`http://localhost:9200/${index}/_search`, {
          size: 1000,
          _source: ['sentiment', 'risk_level']
        })
        const hits = res.data.hits.hits
        hits.forEach(hit => {
          const s = (hit._source.sentiment || '').toLowerCase()
          const r = (hit._source.risk_level || '').toLowerCase()
          if (['positive', 'negative', 'neutral'].includes(s)) this.sentimentData[s]++
          if (['high', 'medium', 'low'].includes(r)) this.riskData[index.replace('_osint','')][r]++
        })
      }
    },
    drawCharts() {
      const sentimentCtx = document.getElementById('sentimentChart')
      new Chart(sentimentCtx, {
        type: 'pie',
        data: {
          labels: ['إيجابي', 'سلبي', 'محايد'],
          datasets: [{
            data: [
              this.sentimentData.positive,
              this.sentimentData.negative,
              this.sentimentData.neutral
            ]
          }]
        }
      })

      const riskCtx = document.getElementById('riskChart')
      new Chart(riskCtx, {
        type: 'bar',
        data: {
          labels: ['Snapchat', 'TikTok', 'Instagram'],
          datasets: [
            {
              label: 'خطر مرتفع',
              data: [
                this.riskData.snapchat.high,
                this.riskData.tiktok.high,
                this.riskData.instagram.high
              ]
            },
            {
              label: 'خطر متوسط',
              data: [
                this.riskData.snapchat.medium,
                this.riskData.tiktok.medium,
                this.riskData.instagram.medium
              ]
            },
            {
              label: 'خطر منخفض',
              data: [
                this.riskData.snapchat.low,
                this.riskData.tiktok.low,
                this.riskData.instagram.low
              ]
            }
          ]
        }
      })
    }
  },
  async mounted() {
    await this.fetchData()
    this.drawCharts()
  }
}
</script>

<style scoped>
.analytics-container {
  padding: 2rem;
  direction: rtl;
  font-family: "Cairo", sans-serif;
}
.charts {
  display: flex;
  flex-wrap: wrap;
  gap: 2rem;
}
.chart {
  flex: 1;
  min-width: 300px;
}
</style>
