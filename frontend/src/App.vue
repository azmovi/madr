<script setup>
import HelloWorld from './components/HelloWorld.vue'
</script>

<template>
  <header>
      <h1>MADR: Meu Acervo Digital de Romancistas</h1>
      <div class="user-session">
          <button @click=''></button> 
      </div>
  </header>

  <main>
     <!-- <HelloWorld /> -->
     ola
  </main>
</template>

<style scoped>
header{
    position: fixed;
    top: 0;
    margin: 3%;

    display: grid;
    grid-auto-flow: column;
    
}
.user-session{
    border: 2px solid;
    margin: 5%;
}

main{
    border: 2px solid;
    margin-top: 15%;
}
</style>
