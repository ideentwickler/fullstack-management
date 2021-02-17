<template>
  <v-container fluid>
    <v-card class="ma-3 pa-3">
      <v-card-title primary-title>
        <div class="headline primary--text">Create Store</div>
      </v-card-title>
      <v-card-text>
        <template>
          <v-form
            v-model="valid"
            ref="form"
            lazy-validation
          >
            <v-text-field
              label="Internal ID"
              v-model="internalId"
              type="number"
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
                  :value="option.name"
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
import { IStore, IStoreCreate, IStoreUpdate } from '@/interfaces';
import { dispatchCreateStore, dispatchGetStores, dispatchUpdateStore } from '@/store/user/actions';
import { readUserOneStore } from '@/store/user/getters';

@Component
export default class EditUser extends Vue {
  public valid = true;
  public name: string = '';
  public internalId: number = 0;
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
  }

  public cancel() {
    this.$router.back();
  }

  public async submit() {
    if (await this.$validator.validateAll()) {
      const createStore: IStoreCreate = {
        support: this.support,
        name: this.name,
        internal_id: this.internalId,
      };

      await dispatchCreateStore(this.$store, createStore);
      await this.$router.push({path: `/main/stores/view/${this.internalId}` });
    }
  }

}
</script>


