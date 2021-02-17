<template>
  <div>
    <v-toolbar light>
      <v-toolbar-title>
        Users
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn color="second_ary" to="/main/admin/users/create"><v-icon>person_add</v-icon> &nbsp;&nbsp;Create User</v-btn>
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
    <v-data-table :headers="headers" :items="users" :search="search" :rows-per-page-items="[25,50,75,100]">
      <template slot="items" slot-scope="props">
        <td>{{ props.item.email }}</td>
        <td>{{ props.item.first_name }}</td>
        <td>{{ props.item.last_name }}</td>
        <td><v-icon v-if="props.item.is_active">checkmark</v-icon></td>
        <td><v-icon v-if="props.item.is_superuser">checkmark</v-icon></td>
        <td class="justify-center layout px-0">
          <v-tooltip top>
            <span>Edit</span>
            <v-btn slot="activator" flat :to="{name: 'main-admin-users-edit', params: {id: props.item.id}}">
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
import { IUserProfile } from '@/interfaces';
import { readAdminUsers } from '@/store/admin/getters';
import { dispatchGetUsers } from '@/store/admin/actions';

@Component
export default class AdminUsers extends Vue {
  public search = '';
  public headers = [
    {
      text: 'Email',
      sortable: true,
      value: 'email',
      align: 'left',
    },
    {
      text: 'First Name',
      sortable: true,
      value: 'first_name',
      align: 'left',
    },
    {
      text: 'Last Name',
      sortable: true,
      value: 'last_name',
      align: 'left',
    },
    {
      text: 'Is Active',
      sortable: true,
      value: 'isActive',
      align: 'left',
    },
    {
      text: 'Is Superuser',
      sortable: true,
      value: 'isSuperuser',
      align: 'left',
    },
    {
      text: 'Actions',
      value: 'id',
    },
  ];
  get users() {
    return readAdminUsers(this.$store);
  }

  public async mounted() {
    await dispatchGetUsers(this.$store);
  }
}
</script>
