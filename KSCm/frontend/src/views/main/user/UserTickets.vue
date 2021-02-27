<template>
  <div>
    <v-toolbar light>
      <v-toolbar-title>
        Tickets
      </v-toolbar-title>
      <v-spacer></v-spacer>
       <ImportTicketDialog :key="ticketRefreshKey" />
    </v-toolbar>
    <v-card-title>
      <v-spacer></v-spacer>
    </v-card-title>
    <v-data-table :disable-initial-sort="true" :no-data-text="noData" :headers="headers" :items="tickets" :pagination.sync="pagination" :total-items="totalTickets" :loading="loading" :rows-per-page-items="[15, 30, 50, 100]">
      <template slot="items" slot-scope="props">
        <td>{{ props.item.ticket_id }}</td>
        <td>{{ props.item.customer_name.toLocaleUpperCase() }}</td>
        <td>{{ props.item.contract_nr }}</td>
        <td>{{ store(props.item.store_internal_id).name }}</td>
        <td>{{ props.item.kind }}</td>
        <td>{{ props.item.status }}</td>
        <td>{{ owner(props.item.owner_id).last_name }}</td>
        <td>{{ convertDate(props.item.created_at) }}</td>

        <td>
          <v-icon v-if="props.item.support === 0" >close</v-icon>
          <v-icon v-if="props.item.support > 0">checkmark</v-icon>
          </td>
        <td class="justify-center layout px-0">
          <v-tooltip top>
            <span>View</span>
            <v-btn slot="activator" flat :to="{name: 'stores-store-view', params: {id: props.item.ticket_id}}">
              <v-icon color="green">pageview</v-icon>
            </v-btn>
          </v-tooltip>
          <v-tooltip top>
            <span>Edit</span>
            <v-btn slot="activator" flat :to="{name: 'stores-store-edit', params: {id: props.item.ticket_id}}">
              <v-icon>edit</v-icon>
            </v-btn>
          </v-tooltip>
        </td>
      </template>
    </v-data-table>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Watch } from 'vue-property-decorator';
import { Store } from 'vuex';
import { ITicket } from '@/interfaces/ticket';
import { dispatchGetStores } from '@/store/user/actions';
import { readAdminOneUser } from '@/store/admin/getters';
import { dispatchGetUsers } from '@/store/admin/actions';
import { readUserOneStore } from '@/store/user/getters';
import { api } from '@/api';
import { readToken } from '@/store/main/getters';
import ImportTicketDialog from '@/components/ImportTicketDialog.vue';


interface Pagination {
  sortBy?: any;
  descending?: boolean | undefined;
  page?: number;
  rowsPerPage?: number;
}

interface Data {
  items: ITicket[];
  total: number;
}

@Component({
  components: { ImportTicketDialog },
})
export default class AdminUsers extends Vue {
  public ticketRefreshKey = 0;
  public search = '';
  public totalTickets = 0;
  public loading = true;
  public tickets = [];
  public items = [];
  public page = 1;
  public pagination: Pagination  = {
    page: 1,
    rowsPerPage: 15,
    descending: false,
    sortBy: '',
  };
  public noData = '...';
  public headers = [
    {
      text: 'Ticket ID',
      sortable: true,
      value: 'ticket_id',
      align: 'left',
    },
    {
      text: 'Customer',
      sortable: true,
      value: 'customer_name',
      align: 'left',
    },
    {
      text: 'Contract Nr',
      sortable: true,
      value: 'contract_nr',
      align: 'left',
    },
    {
      text: 'Store',
      sortable: true,
      value: 'store_internal_id',
      align: 'left',
    },
    {
      text: 'Kind',
      sortable: true,
      value: 'kind',
      align: 'left',
    },
    {
      text: 'Status',
      sortable: true,
      value: 'status',
      align: 'left',
    },
    {
      text: 'Owner',
      sortable: true,
      value: 'owner_id',
      align: 'left',
    },
    {
      text: 'Created',
      sortable: true,
      value: 'created_at',
      align: 'left',
    },
    {
      text: 'Actions',
      sortable: false,
      value: 'actions',
      align: 'right',
    },
  ];

  public owner(ownerId: number) {
    return readAdminOneUser(this.$store)(+ownerId);
  }

  public store(storeId: number) {
    return readUserOneStore(this.$store)(+storeId);
  }

  get getUserToken() {
    return readToken(this.$store);
  }

  public convertDate(date) {
    return new Date(date).toLocaleDateString(
        'de-de',
        {
          year: 'numeric',
          month: 'long',
          day: 'numeric',
        },
    );
  }

  @Watch('ticketRefreshKey', {deep: true})
  @Watch('pagination', {deep: true})
  public handler() {
    this.getPagination()
    .then((data) => {
      this.tickets = data.items;
      this.totalTickets = data.total;
    });
  }


  public async getPagination(): Promise<any> {
    this.loading = true;
    return new Promise((resolve, reject) => {
      const { sortBy, descending, page, rowsPerPage } = this.pagination;

      if (page) {
        this.page = page - 1;
      }

      api.getTickets(this.getUserToken, this.page, rowsPerPage, sortBy, descending)
      .then((value) => {
        const items = value.data.items;
        const total = value.data.total;

        setTimeout(() => {
          this.loading = false;
          resolve({items, total});
        }, 1000);

      });

    });
  }

  public async mounted() {
    await dispatchGetUsers(this.$store);
    await dispatchGetStores(this.$store);
  }


}
</script>
