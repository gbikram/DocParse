<template>
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
  <table>
</template>

<script>
export default {
 props: [
   'macroIocs'
   ]
}
</script>