<template>
  <v-container fluid>
    <v-card class="ma-3 pa-3">
      <v-card-title primary-title>
        <div class="headline primary--text">Edit Store</div>
      </v-card-title>
      <v-card-text>
        <template>
          <div class="my-3">
            <div class="subheading secondary--text text--lighten-2">Name</div>
            <div
              class="title primary--text text--darken-2"
              v-if="oneStore"
            >{{oneStore.name}}</div>
            <div
              class="title primary--text text--darken-2"
              v-else
            >-----</div>
          </div>
          <v-form
            v-model="valid"
            ref="form"
            lazy-validation
          >
            <v-text-field
              label="Internal ID"
              v-model="internalId"
              required
            ></v-text-field>
            <v-text-field
              label="Name"
              v-model="name"
              required
            ></v-text-field>
            <v-radio-group v-model="support">
              <v-radio
                  v-for="option in supportOptions"
                  :key="option.value"
                  :label="` ${option.name}`"
                  :value="option.value"
                  :selected="support"
                  color="red darken-3"
              ></v-radio>
            </v-radio-group>
          </v-form>
        </template>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn @click="cancel">Cancel</v-btn>
        <v-btn @click="reset">Reset</v-btn>
        <v-btn
            @click="submit"
            :disabled="!valid"
        >
          Save
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { IStore, IStoreUpdate } from '@/interfaces';
import {dispatchGetStores, dispatchUpdateStore} from '@/store/user/actions';
import { readUserOneStore } from '@/store/user/getters';

@Component
export default class EditUser extends Vue {
  public valid = true;
  public name: string = '';
  public internalId: number = 5;
  public support: number = 0;
  public supportOptions = [
    {name: 'DISABLED', value: 0},
    {name: 'CLAIM SUPPORT', value: 1},
    {name: 'FULL SUPPORT', value: 2},
  ];

  public async mounted() {
    await dispatchGetStores(this.$store);
    this.reset();
  }

  public reset() {
    this.name = '';
    this.internalId = 0;
    this.support = 0;
    this.$validator.reset();
    if (this.oneStore) {
      this.name = this.oneStore.name;
      this.internalId = this.oneStore.internal_id;
      this.support = this.oneStore.support;
    }
  }

  public cancel() {
    this.$router.back();
  }

  public async submit() {
    if (await this.$validator.validateAll()) {
      const updatedStore: IStoreUpdate = {};
      if (this.name) {
        updatedStore.name = this.name;
      }
      if (this.internalId) {
        updatedStore.internal_id = this.internalId;
      }
      updatedStore.support = this.support;
      await dispatchUpdateStore(this.$store, { id: this.oneStore!.internal_id, store: updatedStore});
      await this.$router.push({path: `/main/stores/view/${this.internalId}` });
    }
  }

  get oneStore() {
    return readUserOneStore(this.$store)(+this.$router.currentRoute.params.id);
  }
}
</script>


