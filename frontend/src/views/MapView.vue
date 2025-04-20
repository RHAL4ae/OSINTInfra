<template>
  <div class="map-controls">
    <button @click="toggleHeatmap">{{ showHeatmap ? 'عرض النقاط' : 'عرض الخريطة الحرارية' }}</button>
    <div id="map" class="map-view"></div>
  </div>
</template>

<script>
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import 'leaflet.heat'
import axios from 'axios'

export default {
  name: 'MapView',
  data() {
    return {
      map: null,
      heat: null,
      showHeatmap: false,
      markers: []
    }
  },
  mounted() {
    this.map = L.map('map').setView([25.4052, 55.5136], 10)

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OpenStreetMap contributors'
    }).addTo(this.map)

    this.loadData()
  },
  methods: {
    toggleHeatmap() {
      this.showHeatmap = !this.showHeatmap
      this.refreshLayers()
    },
    async loadData() {
      const indices = ['snapchat_osint', 'tiktok_osint', 'instagram_osint']
      let heatData = []
      for (let index of indices) {
        const res = await axios.post(`http://localhost:9200/${index}/_search`, {
          size: 500,
          query: {
            exists: { field: "location" }
          }
        })
        const hits = res.data.hits.hits
        hits.forEach(hit => {
          const loc = hit._source.location
          const risk = (hit._source.risk_level || '').toLowerCase()
          const sentiment = (hit._source.sentiment || '').toLowerCase()
          const weight = risk === 'high' ? 3 : risk === 'medium' ? 2 : 1
          heatData.push([loc.lat, loc.lon, weight])

          const marker = L.circleMarker([loc.lat, loc.lon], {
            color: risk === 'high' ? 'red' : risk === 'medium' ? 'orange' : 'green',
            radius: 8
          }).bindPopup(\`<b>المنصة:</b> \${index.replace('_osint','')}<br><b>مشاعر:</b> \${sentiment}<br><b>مخاطر:</b> \${risk}\`)

          this.markers.push(marker)
        })
      }

      this.heat = L.heatLayer(heatData, { radius: 25, blur: 15 })
      this.refreshLayers()
    },
    refreshLayers() {
      if (this.showHeatmap) {
        this.markers.forEach(m => m.remove())
        this.heat.addTo(this.map)
      } else {
        if (this.map.hasLayer(this.heat)) this.heat.remove()
        this.markers.forEach(m => m.addTo(this.map))
      }
    }
  }
}
</script>

<style scoped>
.map-controls {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding: 1rem;
}
.map-view {
  height: 90vh;
  width: 100%;
}
button {
  width: 200px;
  padding: 10px;
  font-weight: bold;
  cursor: pointer;
  align-self: flex-end;
}
</style>
