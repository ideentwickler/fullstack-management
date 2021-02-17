<template>
  <div>
    <v-toolbar light>
      <v-toolbar-title>
        Stores
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn color="second_ary" to="/main/stores/create">Create Store</v-btn>
    </v-toolbar>
    <v-card-title>

      <v-spacer></v-spacer>
      <v-text-field
        v-model="search"
        append-icon="search"
        label="Suche..."
        single-line
        hide-details
      ></v-text-field>
    </v-card-title>
    <v-data-table :headers="headers" :items="stores" :search="search" :rows-per-page-items="[25,50,75,100]">
      <template slot="items" slot-scope="props">
        <td>{{ props.item.internal_id }}</td>
        <td>{{ props.item.name }}</td>
        <td>
          <v-icon v-if="props.item.support === 0" >close</v-icon>
          <v-icon v-if="props.item.support > 0">checkmark</v-icon>
          </td>
        <td class="justify-center layout px-0">
          <v-tooltip top>
            <span>View</span>
            <v-btn slot="activator" flat :to="{name: 'stores-store-view', params: {id: props.item.internal_id}}">
              <v-icon color="green">pageview</v-icon>
            </v-btn>
          </v-tooltip>
          <v-tooltip top>
            <span>Edit</span>
            <v-btn slot="activator" flat :to="{name: 'stores-store-edit', params: {id: props.item.internal_id}}">
              <v-icon>edit</v-icon>
            </v-btn>
          </v-tooltip>
        </td>
      </template>
    </v-data-table>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { Store } from 'vuex';
import { IStore } from '@/interfaces';
import {readUserStores} from '@/store/user/getters';
import {dispatchGetStores} from '@/store/user/actions';

@Component
export default class AdminUsers extends Vue {
  public search = '';
  public headers = [
    {
      text: 'Internal ID',
      sortable: true,
      value: 'internal_id',
      align: 'left',
      width: '10%',
    },
    {
      text: 'Name',
      sortable: true,
      value: 'name',
      align: 'left',
      width: '20%',
    },
    {
      text: 'Support',
      sortable: true,
      value: 'support',
      align: 'left',
    },
    {
      text: 'Actions',
      value: 'id',
      align: 'center',
    },
  ];
  get stores() {
    return readUserStores(this.$store);
  }

  public async mounted() {
    await dispatchGetStores(this.$store);
  }
}
</script>
