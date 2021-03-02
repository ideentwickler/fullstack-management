<template>
  <v-card>
    <v-card-title class="headline second_ary">Ticket Performance</v-card-title>
    <v-card-text>

      <v-container fluid>
    <v-flex xs12 sm12 v-if="!loading" class="justify-center">
      <LineChart :height=100 :chart-data="dataCollection"></LineChart>
    </v-flex>
    <v-flex xs12 sm12 v-if="loading" justify-center>
      <v-progress-circular
      :size="50"
      color="second_ary"
      indeterminate
    ></v-progress-circular>
    </v-flex>

  </v-container>

    </v-card-text>
    <v-card-actions>
        <v-select
          :items="staticYears"
          v-model="selectedYear"
          label="Year"
        ></v-select>
        <v-select
          :items="staticStores"
          v-model="selectedStore"
          label="Store">
      </v-select>
    </v-card-actions>
  </v-card>


</template>

<script lang="ts">
import {Component, Vue, Watch} from 'vue-property-decorator';
import { api } from '@/api';
import { readToken } from '@/store/main/getters';
import { Bar } from 'vue-chartjs';
import LineChart from '@/components/charts/BarChart';

interface BenchmarkStore {
  claims: number;
  commission: number;
}

interface BillsStore {
  bill: number;
  count: number;
  discharge: number;
  total: number;
}

interface CountsStore {
  CLAIM: number[];
  COMMISSION: number[];
  IMPORTED: number[];
  INCOMPLETE: number[];
  TOTAL: number[];
}

interface ProcessingStore {
  ANSWERED_QUESTION: number[];
  CLOSED: number[];
  IN_PROGRESS: number[];
  NEW: number[];
  OPEN_QUESTION: number[];
  ORDERED: number[];
}

interface StaticStore {
  benchmarks: BenchmarkStore;
  bills: BillsStore;
  counts: CountsStore;
  headline: any;
  months: string[];
  plot: null;
  processing: ProcessingStore;
}

interface StaticYears {
  year: {
    [key: string]: StaticStore[];
  };
}

@Component({
  components: {LineChart}
})
export default class ImportTicketDialog extends Vue {
  public loading: boolean = true;
  public staticData = {};
  public staticYears: string[] = [];
  public staticStores: string[] = [];
  public monthsNames: string[] = [];
  public monthsCommission: number[] = [];
  public monthsClaims: number[] = [];
  public monthsTotal: number[] = [];
  public selectedYear: number = 1999;
  public selectedStore: string = 'TOTAL';
  public dataCollection = {};

  public getStaticStore(year, store) {
    const data = this.staticData[year][store];
    this.monthsNames = data.months
    this.monthsCommission = data.counts.COMMISSION;
    this.monthsClaims = data.counts.CLAIM;
    this.monthsTotal = data.counts.TOTAL;

    this.dataCollection = {
      labels: this.monthsNames,
      datasets: [
        {
          label: 'Commission',
          backgroundColor: '#89D1FE',
          data: this.monthsCommission,
        },
        {
          label: 'Claims',
          backgroundColor: '#f87979',
          data: this.monthsClaims,
        }
      ],
    }
  }

  @Watch('selectedYear', {deep: true})
  @Watch('selectedStore', {deep: true})
  changeStaticData() {
    console.log("changed selected");
    this.getStaticStore(this.selectedYear, this.selectedStore);
  }

  public async getYears() {
    Object.keys(this.staticData).map((key) => {
      this.staticYears.push(key);
      this.selectedYear = this.staticYears[this.staticYears.length -1];
      Object.keys(this.staticData[key]).map((key) => {
        this.staticStores.push(key);
      })
      this.selectedStore = 'TOTAL';
    })
    console.log(this.staticYears);
    console.log(this.staticStores);
  }

  public async getStaticData() {
    const token = readToken(this.$store);
    api.getStaticData(token)
    .then((value) => {
      this.staticData = value.data;
      this.loading = false;
    })
    .then(() => {
      this.getYears();
    });
  }

    public async mounted() {
      await this.getStaticData();
    }

}
</script>

<style>
  .line-chart {
    display: inline-table;
    width: 1200px;
    height: 500px;
}
</style>