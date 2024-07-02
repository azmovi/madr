<script setup>
import { ref } from 'vue'

const message = ref('')

async function teste() {
    await fetch('http://localhost:8000/')
        .then((res) => res.json())
        .then((json) => message.value = json.message)
        .catch((err) => message.value = err)
};
</script>

<template>
  <div class="basicos">
        <button @click="teste"> Teste </button>
        <p>{{ message }}</p>
  </div>
</template>

<style scoped>
</style>
