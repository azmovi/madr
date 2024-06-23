<script setup lang="ts">
import { ref } from 'vue';

const message = ref('');

async function teste() {
    try {
        const response = await fetch('http://localhost:8000/');
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        const data = await response.json();
        message.value = data.message;
    } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
    }
}
</script>

<template>
    <div class="wrapper">
        <h1>Olá mundo</h1>
        <button @click="teste">Teste de API</button>
        <p>{{ message }}</p>
    </div>
</template>

<style scoped>
/* Estilos locais para o componente */
.wrapper {
    text-align: center;
    margin-top: 20px;
}

button {
    margin-top: 10px;
}
</style>

