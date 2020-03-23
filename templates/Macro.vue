<template>
  <div class="modal" :class="{ 'is-active': viewMacro }">
    <div class="modal-background"></div>
    <div class="modal-card">
      <header class="modal-card-head">
        <p class="modal-card-title">IOCs from Embedded VBA</p>
        <button class="delete" aria-label="close"></button>
      </header>
      <section class="modal-card-body">
        <table class="table" id="macro">
          <thead>
            <tr>
              <th>Type</th>
              <th>Keyword</th>
              <th>Description</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="macroioc in macroiocs">
              <td>${ macroioc.type }</td>
              <td>${ macroioc.keyword }</td>
              <td>${ macroioc.description }</td>
            </tr>
          </tbody>
        </table>
      </section>
      <footer class="modal-card-foot">
        <button class="button is-success" v-on:click="viewMacro = false">Done</button>
      </footer>
    </div>
  </div>
</template>

<script>
export default {
  props: ["macroIocs"]
};
</script>