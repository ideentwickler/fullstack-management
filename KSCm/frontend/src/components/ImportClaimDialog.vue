<template>
  <div class="text-xs-center">
    <v-dialog
      v-model="dialog"
      width="500"
    >
      <template v-slot:activator="{ on }">
        <v-btn
          color="second_ary"
          v-on="on"
        >
          Import Claims
        </v-btn>
      </template>

      <v-card>
        <v-card-title
          class="headline second_ary"
        >
          <h3>Import Claims</h3>
        </v-card-title>

        <v-card-text>

          <v-container grid-list-lg>
            1. Upload
            <v-text-field
                label="Select..."
                @click='onPickFile'
                v-model='fileName'
                prepend-icon="attach_file"
            ></v-text-field>
            <!-- Hidden -->
            <input
                type="file"
                style="display: none"
                ref="fileInput"
                accept="*/*"
                @change="onFilePicked">

            <!-- Kind of logs -->
            <v-progress-linear v-if="this.taskStatus !== '' && this.taskStatus !== 'SUCCESS'" height="20px" color="primary"
                                     :indeterminate="true"></v-progress-linear>
            <v-progress-linear v-if="this.taskStatus == 'SUCCESS'" height="20px" color="primary"
                                     ></v-progress-linear>
            <p>{{ statusMsg }}</p>
          </v-container>

        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
                color="primary"
                @click.stop="onUploadSelectedFileClick"
                :loading="loading"
                v-if="this.taskStatus === ''"
            >UPLOAD
            </v-btn>
          <v-btn
            color="primary"
            flat
            @click="reset"
            v-if="this.taskStatus === ''"
          >
            Exit
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script lang="ts">
import {Component, Vue, Prop} from 'vue-property-decorator';
import { api } from '@/api';
import { readToken } from '@/store/main/getters';

@Component
export default class ImportTicketDialog extends Vue {
  @Prop({default: false})
  public ticketRefreshKey: number | undefined;

  public e1 = 0;
  public fileName = '';
  public url: any = '';
  public fileObject = {lastModifiedDate: null, type: '', size: '', name: ''};
  public cardResult = '';
  public name =  '';
  public size = '';
  public type = '';
  public lastModifiedDate: string | null = '';
  public loading = false;
  public dialog: boolean = false;
  public taskId = '';
  public taskStatus = '';
  public statusMsg = '';

  public reset() {
    this.fileName = '';
    this.url = '';
    this.fileObject = {lastModifiedDate: null, type: '', size: '', name: ''};
    this.cardResult = '';
    this.name = '';
    this.size = '';
    this.type = '';
    this.loading = false;
    this.taskId = '';
    this.taskStatus = '';
    this.statusMsg = '';
    this.dialog = false;
  }

  public resetAndRefresh() {
    setTimeout(() => {
      this.statusMsg = 'Preparing for a re-load...';
    }, 2500);
    this.reset();
    /* tslint:disable:no-string-literal */
    this.$parent.$parent['ticketRefreshKey'] = 1;
    /* tslint:enable:no-string-literal */
  }

  public onPickFile(): void {
      return (this.$refs.fileInput as HTMLElement).click();
    }

  public onFilePicked(event) {
      const files = event.target.files;
      if (files[0] !== undefined) {
        this.fileName = files[0].name;
        // Check validity of file
        if (this.fileName.lastIndexOf('.') <= 0) {
          return;
        }
        // If valid, continue
        const fr = new FileReader();
        fr.readAsDataURL(files[0]);
        fr.addEventListener('load', () => {
          this.url = fr.result;
          this.fileObject = files[0]; // this is an file that can be sent to server...

        });
      } else {
        this.fileName = '';
        this.fileObject = {lastModifiedDate: null, type: '', size: '', name: ''};
        this.url = '';
      }
    }

    public getTaskStatus(taskId: string) {
      const token = readToken(this.$store);
      const retryTaskInterval = setInterval(() => {
        api.getTaskStatus(token, taskId)
        .then((task) => {
          const status = task.data.result;
          if (status === undefined) {
            this.statusMsg = 'Sorry something went wrong... Please try again';
            clearInterval(retryTaskInterval);
            setTimeout(() => {
              this.reset();
            }, 3000);
          }
          if (status === 'STARTED') {
            this.taskStatus = 'STARTED';
            this.statusMsg = 'Task started to process data...';
          }
          if (status === 'PROGRESS') {
            this.taskStatus = 'PROGRESS';
            this.statusMsg = 'Task progressing data... This can take a while';
          }
          if (status === 'SUCCESS') {
            clearInterval(retryTaskInterval);
            setTimeout(() => {
              this.taskStatus = 'SUCCESS';
              this.statusMsg = 'Task successfully done! ';
              this.resetAndRefresh();
            }, 2500);
          }
          if (status === 'PENDING') {
            clearInterval(retryTaskInterval);
            setTimeout(() => {
              this.taskStatus = 'PENDING';
              this.statusMsg = 'Sorry something went wrong... ';
              this.resetAndRefresh();
            }, 2500);
          }
        });
      }, 2500);
    }

    public createTask(mediaId: string) {
      const token = readToken(this.$store);
      api.createTask(token, mediaId)
      .then((value) => {
        this.taskId = value.data.task_id;
        setTimeout(() => {
          this.statusMsg = `Running task ${this.taskId}`;
        }, 2500);
        this.getTaskStatus(this.taskId);
      });
    }

    public fileObjectToUpload(fileObject) {
      const token = readToken(this.$store);
      const formData = new FormData();
      formData.append('file', fileObject);
      this.statusMsg = 'Uploading file...';

      api.postFileObject(token, formData, 'CLAIMS')
      .then((value) => {
        const mediaId = value.data.id;

        setTimeout(() => {
          this.statusMsg = 'File successfully uploaded...';
          this.createTask(mediaId);
        }, 2500);
      });

      return;
    }

    public onUploadSelectedFileClick() {
      // A file is not chosen!
      // DO YOUR JOB HERE with fileObjectToUpload
      // https://developer.mozilla.org/en-US/docs/Web/API/File/File
      this.name = this.fileObject.name;
      this.size = this.fileObject.size;
      this.type = this.fileObject.type;
      this.lastModifiedDate = this.fileObject.lastModifiedDate;
      // VALIDATOR
      if (!this.fileObject) {
        this.statusMsg = 'Please select a file';
        return;
      }
      if (!this.type.includes('application/vnd.openxmlformats')) {
        this.statusMsg = 'Invalid file type...';
        return;
      }

      this.loading = true;
      // DO YOUR JOB HERE with fileObjectToUpload
      this.fileObjectToUpload(this.fileObject);
      this.loading = false;
    }

}
</script>

<style scoped>

</style>