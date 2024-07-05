<script setup>
import { RouterLink } from "vue-router";
</script>

<template>
    <header>
        <nav>
            <RouterLink :to="{ name: 'home' }">
                <div class="botao home">
                    <h1>MADR</h1>
                </div>
            </RouterLink>

            <ul>
                <RouterLink :to="{ name: 'livros' }">
                    <li class="botao item"> Livros </li>
                </RouterLink>
                <RouterLink :to="{ name: 'romancistas' }">
                    <li class="botao item"> Romancistas </li>
                </RouterLink>
            </ul>

            <RouterLink :to="{ name: 'conta' }">
                <div>
                    <p class="botao conta"> Sign In/Sign Up </p>
                </div>
            </RouterLink>
        </nav>
    </header>
</template>

<style scoped>
nav{
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-left: 10%;
    margin-right: 10%;
}

ul{
    display: flex;
    list-style: none;
    gap: 15%;
}

</style>
