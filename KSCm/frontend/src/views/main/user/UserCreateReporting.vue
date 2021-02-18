<template>
  <v-container fluid>
    <v-card class="ma-3 pa-3">
      <v-card-title primary-title>
        <div class="headline primary--text">New Reporting</div>
      </v-card-title>
      <v-card-text>
        <template>

          <v-stepper v-model="e1">
            <v-stepper-header>
              <v-stepper-step :complete="e1 > 1" step="1">Select Stores
              </v-stepper-step>

              <v-divider></v-divider>

              <v-stepper-step :complete="e1 > 2" step="2">Select Period
              </v-stepper-step>

              <v-divider></v-divider>

              <v-stepper-step step="3">Finally</v-stepper-step>
            </v-stepper-header>

            <v-stepper-items>
              <v-stepper-content step="1">
                <v-card
                    class="mb-5"
                    color="white lighten-1"
                >
                  <v-card-title><h2>Select Stores</h2></v-card-title>
                  <v-btn
                      flat
                      @click="autoSelectAllStores"
                  >
                    Select All
                  </v-btn>
                  <v-container fluid>
                    <v-layout row wrap>
                      <v-flex
                          v-for="store in supportedStores"
                          :key="store.internal_id"
                          xs3
                      >
                        <v-card flat tile>
                          <v-checkbox
                              v-model="selectedStores"
                              :label="store.name"
                              color="primary"
                              :value="store.internal_id"
                          ></v-checkbox>
                        </v-card>
                      </v-flex>
                    </v-layout>
                  </v-container>
                  {{ selectedStores.length }} selected
                </v-card>

                <v-btn
                    v-if="selectedStores.length !== 0"
                    color="second_ary"
                    @click="e1 = 2"
                >
                  Continue
                </v-btn>
                <v-btn
                    v-else disabled>Continue
                </v-btn>

              </v-stepper-content>

              <v-stepper-content step="2">
                <v-card
                    class="mb-5"
                    color="white lighten-1"
                    height=""
                >

                  <div>
                    <v-date-picker color="primary" no-title multiple full-width
                                   v-model="picker" type="month"></v-date-picker>
                  </div>

                </v-card>

                <v-btn
                    v-if="picker.length === 2"
                    color="second_ary"
                    @click="e1 = 3"
                >
                  Continue
                </v-btn>
                <v-btn v-else disabled>Continue</v-btn>
                <v-btn
                    flat
                    @click="e1 = 1"
                >
                  Back
                </v-btn>

              </v-stepper-content>

              <v-stepper-content step="3">
                <v-card
                    class="mb-5"
                    color="white lighten-1"
                >

                  <v-container fluid>
                    <v-layout row wrap>
                      <v-flex
                          xs4>
                        <v-text-field
                            v-model="reportingTitle"
                            label="Titel"
                            prepend-icon="title"
                        ></v-text-field>
                      </v-flex>
                      <v-flex xs2></v-flex>
                      <v-flex xs4>
                        <v-checkbox
                            v-model="sendReportingAsMail"
                            prepend-icon="settings_suggest"
                            label="`Send Report via E-Mail"
                        ></v-checkbox>
                        <v-text-field
                            v-model="eMailReciepent"
                            prepend-icon="email"
                            v-if="sendReportingAsMail"
                            label=""
                          ></v-text-field>
                      </v-flex>
                    </v-layout>
                  </v-container>

                </v-card>

                <div class="text-center">
                  <v-dialog
                      v-model="dialog"
                      width="500"
                  >
                    <template v-slot:activator="{ on, attrs }">
                      <v-btn
                          color="second_ary"
                          v-bind="attrs"
                          v-on="on"
                          @click="submit"
                      >
                        Create Report
                      </v-btn>
                    </template>

                    <v-card>
                      <v-card-title class="headline grey lighten-2">
                        <h2 v-if="loading">Processing Data...</h2>
                        <h2 v-else>Successfully created...</h2>
                      </v-card-title>

                      <v-card-text>
                        <v-progress-linear v-if="loading" height="20px" color="second_ary"
                                     :indeterminate="true"></v-progress-linear>
                        <v-progress-linear v-if="!loading" height="20px"
                                           color="second_ary"></v-progress-linear>
                      </v-card-text>

                      <v-divider></v-divider>

                      <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn
                            color="primary"
                            text
                            @click="dialog = false"
                        >
                          Close
                        </v-btn>
                      </v-card-actions>
                    </v-card>
                  </v-dialog>
                  <v-btn
                    flat
                    @click="e1 = 2"
                >
                  Back
                </v-btn>
                </div>



              </v-stepper-content>
            </v-stepper-items>
          </v-stepper>

        </template>
      </v-card-text>
      <v-card-actions>

      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script lang="ts">
import {Component, Vue} from 'vue-property-decorator';
import {IReportingFileCreate} from '@/interfaces';
import {
  dispatchGetFile,
  dispatchGetStores,
} from '@/store/user/actions';
import {
  readUserSupportedStores,
} from '@/store/user/getters';
import {readToken} from "@/store/main/getters";


@Component
export default class EditUser extends Vue {
  public e1: number = 0;
  public menu: boolean = false;
  public loading: boolean = true;
  public dialog: boolean = false;
  public selectedStores: string[] = [];
  public picker: string[] = [];
  public endMonth: string = '';
  public startMonth: string = '';
  public startEndYear: string = '';
  public reportingTitle: string = '';
  public sendReportingAsMail: boolean = false;
  public eMailReciepent: string = '';

  public async mounted() {
    await dispatchGetStores(this.$store);
    this.reset();
  }

  public async autoSelectAllStores() {
    this.selectedStores = [];
    for (const key in this.supportedStores) {
      if (this.supportedStores.hasOwnProperty(key)) {
        const store = this.supportedStores[key];
        this.selectedStores.push(store.internal_id);
      }
    }
  }

  get supportedStores() {
    return readUserSupportedStores(this.$store);
  }

  public create() {
    this.e1 = 3;
    this.submit();
  }

  get userToken() {
    return readToken(this.$store);
  }

  public async submit() {
    this.loading = true;
    if (this.picker.length === 2 && this.selectedStores.length !== 0) {
      this.startEndYear = this.picker[0].split('-')[0];
      this.startMonth = this.picker[0].split('-')[1];
      this.endMonth = this.picker[1].split('-')[1];

      if (this.startEndYear && this.startMonth && this.endMonth) {
        const createReportingFile: IReportingFileCreate = {
          year: this.startEndYear,
          month_start: this.startMonth,
          month_end: this.endMonth,
          stores: this.selectedStores,
          title: this.reportingTitle,
        };
        if (this.sendReportingAsMail && this.eMailReciepent !== '') {
          createReportingFile.email_reciepent = this.eMailReciepent;
        }

        const res = await dispatchGetFile(this.$store, createReportingFile);
        if (res) {
          this.loading = false;
          window.open(`http://localhost/views/reporting?token=${this.userToken}`, '', 'width=1200px, height=842px');
        }
      }
    }
  }

  public reset() {
    this.$validator.reset();
  }

  public cancel() {
    this.$router.back();
  }

}
</script>


