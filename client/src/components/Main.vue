<template>
  <div class="container">

    <!--Upload Section-->
    <section class="section">
      <h1 class="title is-1">DocParse</h1>
      <h2 class="subtitle">Scan files for IOCs - currently supports DOC, DOCX, EML</h2>
      <div class="field is-horizontal">
        <div class="file has-name is-info">
          <label class="file-label">
            <input class="file-input" type="file" ref="file" v-on:change="handleFileUpload()" />
            <span class="file-cta">
              <span class="file-icon">
                <i class="fas fa-upload"></i>
              </span>
              <span class="file-label">Browse File...</span>
            </span>
            <span class="file-name" v-if="selectorFileName">{{ selectorFileName }}</span>
            <span class="file-name" v-else>No file selected</span>
          </label>
        </div>
        <button class="button" v-on:click="submitFile()">Upload</button>
      </div>
    </section>

    <!--Output Section-->
    <section class="section" v-if="primaryFileData">
      <div class="content">
        <h4 class="subtitle is-4">File Details</h4>
        <table class="table" id="genericTable">
          <tbody>
            <tr>
              <td>
                <label class="label">Name</label>
              </td>
              <td>{{ primaryFileData.file_name }}</td>
            </tr>
            <tr>
              <td>
                <label class="label">File Type</label>
              </td>
              <td>{{ primaryFileData.file_type.toUpperCase() }}</td>
            </tr>
            <tr></tr>
          </tbody>
        </table>

        <!---Email Data-->
        <div class="content" v-if="primaryFileData.file_type === 'eml'">
          <div class="field" v-if="primaryFileData.body_urls.length > 0">
            <label class="label">URLs from Email Body</label>
            <ul id="bodyUrls">
              <li v-for="url in primaryFileData.body_urls">{{ url }}</li>
            </ul>
          </div>
          <div class="content" v-if="primaryFileData.headers">
            <button class="button is-info is-outline" v-on:click="emlHeadToggle = true">Headers</button>
            <div class="modal" :class="{ 'is-active': emlHeadToggle }">
              <div class="modal-background"></div>
              <div class="modal-card">
                <header class="modal-card-head">
                  <p class="modal-card-title">Email Header</p>
                  <button class="delete" aria-label="close"></button>
                </header>
                <section class="modal-card-body">
                  <table class="table">
                    <tbody>
                      <tr v-for="(headerValue, headerKey) in primaryFileData.headers">
                        <td>{{ headerKey }} :</td>
                        <td>{{ headerValue[0] }}</td>
                      </tr>
                    </tbody>
                  </table>
                </section>
                <footer class="modal-card-foot">
                  <button class="button is-success" v-on:click="emlHeadToggle = false">Done</button>
                </footer>
              </div>
            </div>
          </div>

          <div class="content" v-if="primaryFileData.attachments">
            <label class="label">Attachments</label>
            <article class="message" v-for="attachment in primaryFileData.attachments">
              <div
                class="message-header"
                v-on:click="attachment.contracted = !attachment.contracted"
              >
                <p>{{ attachment.file_name }}</p>
                <button class="button" id="dropdown">
                  <span class="icon">
                    <i class="far fa-caret-square-down"></i>
                  </span>
                </button>
              </div>
              <div
                class="message-body"
                id="attachment"
                :class="{'contracted': attachment.contracted}"
              >
                <div class="field is-horizontal" v-for="(value, hash) in attachment.hash">
                  <label class="label">{{ hash.toUpperCase() }} :</label>
                  <p>{{ value }}</p>
                </div>
                <div
                  class="content"
                  v-if="(attachment.file_name.endsWith('docx') || attachment.file_name.endsWith('doc')) && attachment.macros"
                >
                  <button
                    class="button is-info is-outline"
                    v-on:click="styleActive.display = 'block'"
                  >Embedded VBA</button>
                  <macro
                    :macroiocs="attachment.macros"
                    :style="styleActive"
                    @show-vba="styleActive.display = 'none'"
                  ></macro>
                </div>
              </div>
            </article>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import axios from 'axios';
import bulma from 'bulma';

import Macro from "./Macro.vue";

export default {
    name: 'Main',
    components: {
        Macro
    },
    data() {
        return {
            api_domain: process.env.VUE_APP_API,
            file: '',
            hash: '',
            selectorFileName: null,
            primaryFileData: null,
            url: '',
            viewMacro: false,
            styleActive: {
                display: 'none'
            },
            emlHeadToggle: false,
        }
    },

    methods: {
        handleFileUpload() {
            this.file = this.$refs.file.files[0];
            this.selectorFileName = this.file.name;
        },

        // To-do - Submit file to server
        submitFile() {
            let formData = new FormData();
            formData.append('file', this.file);

            axios.post(this.api_domain + '/AnalyzeFile',
                formData,
                {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                }
            ).then(response => {
                var fileData = response.data[this.selectorFileName]
                var primaryFileData = {}
                primaryFileData = {
                    "file_name": this.selectorFileName,
                    "file_type": fileData.file_type
                }
                var fileType = primaryFileData.file_type
                if (fileType === "eml") {                    
                    if(fileData.email_data.attachments) {
                      primaryFileData["attachments"] = fileData.email_data.attachments
                      // Add dropdown state
                      for(var i = 0; i < primaryFileData["attachments"].length; i ++) {
                          primaryFileData["attachments"][i].contracted = false
                      }
                    }

                    primaryFileData["body_urls"] = fileData.email_data.body_urls
                    primaryFileData["headers"] = fileData.email_data.headers

                } else if (fileType === "docx") {
                    primaryFileData["body_iocs"] = fileData.body_iocs
                    primaryFileData["macro_iocs"] = fileData.macro_iocs

                } else if (fileType === "doc") {
                    primaryFileData["macro_iocs"] = fileData.macro_iocs
                }
                this.primaryFileData = primaryFileData
            })
                .catch(error => {
                    console.log(error);
                });
        },
    }
}
</script>

<style>
.button {
    margin-left: 5px;
}

.container {
    margin-top: 5px;
}

.section {
    padding: 1rem 1.5rem;
}

.subtitle.is-4 {
    border-bottom: solid #e6e6e6 1.5px;
}

.label {
    margin-right: 5px;
}

#genericTable {
    width: 50%;
    margin-bottom: 5px;
}

.modal-card {
    width: 60%;
}

.content ul {
    list-style: none;
    margin-left: 0em;
    margin-top: 0em;
}

.content {
    margin-top: 2em;
}

#bodyUrls {
    overflow: auto;
    max-width: 50%;
    max-height: 200px;
}

.contracted {
    display: none !important; 
}

#dropdown {
    background: transparent;
    color: white;
    border: none;
}

.footer {
    position: relative;
    margin-top: 15em;
    left: 0;
    bottom: 0;
    width: 100%;
    text-align: center;
    background-color: #8080804f;
}
</style>
