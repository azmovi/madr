<script setup>
import { RouterLink } from "vue-router";
</script>

<template>
    <header>
        <nav>
            <RouterLink :to="{ name: 'home' }">
                <div class="home">
                    <h1>MADR</h1>
                </div>
            </RouterLink>
            <ul>
                <li class="item"> Livros </li>
                <li class="item"> Romancistas </li>
            </ul>
            <button type="button"> Sign in / Sign up </button>
        </nav>
    </header>
</template>

<style scoped>
nav{
    padding: 5%;
    display: flex;
    align-items: center;
    justify-content: space-between;

}

ul{
    display: flex;
    list-style: none;
    gap: 12%;
}


.home{
  color: #d3d3d3;
}
</style>
