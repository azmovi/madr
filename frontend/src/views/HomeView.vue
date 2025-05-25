<template>
  <div class="home">
    <h1>Bem-vindo ao Site!</h1>
    <ul>
      <li v-for="user in users" :key="user.id">
        {{ user.username }} - {{ user.email }}
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const users = ref([])

onMounted(async () => {
  try {
    const response = await fetch('/api/conta/', {
      method: 'GET',
    })

    if (!response.ok) throw new Error('Erro ao buscar usuários.')

    users.value = await response.json()
  } catch (error) {
    console.error(error)
  }
})
</script>

<style scoped>
</style>
