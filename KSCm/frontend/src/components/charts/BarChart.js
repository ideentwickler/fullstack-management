import { Bar, mixins } from 'vue-chartjs';
const { reactiveProp } = mixins;

export default {
  name: 'LineChart',
  extends: Bar,
  mixins: [reactiveProp],

 async  mounted () {
    // this.chartData is created in the mixin.
    // If you want to pass options please create a local options object
    const options = {
    responsive: true,
    maintainAspectRatio: false,
    cutoutPercentage: 80,
    legend: {
      display: true
    },
    tooltips: {
      enabled: true
    },
    hover: {
      mode: true
    },
    scales: {
        yAxes: [
            {
                ticks: { precision: 0,}
            }
            ]
    },
  }
    this.renderChart(this.chartData, options)
  }
}