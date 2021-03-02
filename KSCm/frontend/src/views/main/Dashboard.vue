<template>
  <div>
  <v-toolbar light>
      <v-toolbar-title>
        Dashboard
      </v-toolbar-title>
      <v-spacer></v-spacer>
    </v-toolbar>

    <v-container grid-list-md text-xs-center fluid>
     <v-layout row wrap>
       <v-flex xs6>
        <StaticDataChart />
      </v-flex>
       <v-flex xs6>
        <v-card>
          <v-card-title class="headline second_ary">Team Chat</v-card-title>
          <v-card-text class="px-0">
          <ul id='messages'>
          </ul>

          </v-card-text>
        </v-card>
      </v-flex>
     </v-layout>

    </v-container>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { Store } from 'vuex';
import { readUserProfile } from '@/store/main/getters';
import StaticDataChart from '@/components/StaticDataChart.vue';
@Component({
  components: {StaticDataChart},
})
export default class Dashboard extends Vue {
  public clientId: number = 0;
  public conn: WebSocket;

  get greetedUser() {
    const userProfile = readUserProfile(this.$store);
    if (userProfile) {
      if (userProfile.first_name) {
        return userProfile.first_name;
      } else {
        return userProfile.email;
      }
    }
  }

  public created() {
    console.log("created...");
    this.clientId = Date.now();
    let ws = new WebSocket(`ws://localhost/api/v1/ws/${this.clientId}`);

    ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                console.log(content);
                console.log("on message");
                messages.appendChild(message)
            };
  }
}
</script>
