<template>
  <div class="conta">
    <form @submit.prevent="handleLogin">
      <h2>Login</h2>
      <input v-model="loginData.email" type="email" placeholder="Email" required />
      <input v-model="loginData.password" type="password" placeholder="Senha" required />
      <button type="submit" :disabled="loading">
        {{ loading ? 'Entrando...' : 'Entrar' }}
      </button>
    </form>

    <form @submit.prevent="handleRegister" style="margin-top: 2rem">
      <h2>Registro</h2>
      <input v-model="registerData.username" type="text" placeholder="Nome de usuário" required />
      <input v-model="registerData.email" type="email" placeholder="Email" required />
      <input v-model="registerData.senha" type="password" placeholder="Senha" required />
      <button type="submit" :disabled="loading">
        {{ loading ? 'Criando...' : 'Criar Conta' }}
      </button>
    </form>

    <div v-if="message" :class="['message', messageType]">
      {{ message }}
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const loading = ref(false)
const message = ref('')
const messageType = ref('') 

const loginData = ref({
  email: '',
  password: ''
})

async function handleLogin() {
  loading.value = true
  message.value = ''
  
  try {
    const res = await fetch('/api/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(loginData.value)
    })

    if (!res.ok) {
      const error = await res.json()
      message.value = `Erro ao entrar: ${error.detail || 'Erro desconhecido'}`
      messageType.value = 'error'
      return
    }

    const data = await res.json()
    message.value = 'Login realizado com sucesso!'
    messageType.value = 'success'
    
    console.log('Token:', data.access_token)
    
  } catch (err) {
    message.value = 'Erro na requisição: ' + err.message
    messageType.value = 'error'
  } finally {
    loading.value = false
  }
}

const registerData = ref({
  username: '',
  email: '',
  senha: '' 
})

async function handleRegister() {
  loading.value = true
  message.value = ''
  
  try {
    const res = await fetch('/api/conta/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(registerData.value)
    })

    if (!res.ok) {
      const error = await res.json()
      message.value = `Erro ao registrar: ${error.detail || 'Erro desconhecido'}`
      messageType.value = 'error'
      return
    }

    const data = await res.json()
    message.value = 'Conta criada com sucesso!'
    messageType.value = 'success'
    
    registerData.value = {
      username: '',
      email: '',
      senha: ''
    }
    
  } catch (err) {
    message.value = 'Erro na requisição: ' + err.message
    messageType.value = 'error'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.conta {
  max-width: 400px;
  margin: auto;
  padding: 2rem;
}

form {
  background: #f9f9f9;
  padding: 1.5rem;
  border-radius: 8px;
  margin-bottom: 1rem;
}

input {
  display: block;
  margin-bottom: 1rem;
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  box-sizing: border-box;
}

input:focus {
  outline: none;
  border-color: #007bff;
}

button {
  padding: 0.75rem 1.5rem;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  width: 100%;
}

button:hover:not(:disabled) {
  background-color: #0056b3;
}

button:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
}

.message {
  margin-top: 1rem;
  padding: 0.75rem;
  border-radius: 4px;
  text-align: center;
}

.message.success {
  background-color: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.message.error {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}
</style>
