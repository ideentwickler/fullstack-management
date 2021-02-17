<template>
  <v-container fluid>
    <v-card class="ma-3 pa-3">
      <v-card-title primary-title>
        <div class="headline primary--text">Store</div>
      </v-card-title>
      <v-card-text>
        <div class="my-4">
          <div class="subheading secondary--text text--lighten-3">Name</div>
          <div class="title primary--text text--darken-2" v-if="oneStore && oneStore.name">{{oneStore.name}}</div>
          <div class="title primary--text text--darken-2" v-else>-----</div>
        </div>
      </v-card-text>
      <v-card-actions>
        <v-btn to="/main/profile/edit">Edit</v-btn>
        <v-btn to="/main/profile/password">Change password</v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { Store } from 'vuex';
import {readUserOneStore} from '@/store/user/getters';

@Component
export default class UserProfile extends Vue {
  get oneStore() {
    return readUserOneStore(this.$store)(+this.$router.currentRoute.params.id);
  }

  public goToEdit() {
    this.$router.push('/main/profile/edit');
  }

  public goToPassword() {
    this.$router.push('/main/profile/password');
  }
}
</script>
