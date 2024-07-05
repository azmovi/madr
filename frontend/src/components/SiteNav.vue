<script setup>
import { RouterLink } from "vue-router";
</script>

<template> <nav>
        <RouterLink :to="{ name: 'home' }">
            <div class="botao">
                <i></i>
                Mader 
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
</template>

<style scoped>
nav{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1%;
    font-size: 20px;
    margin-left: 10%;
    margin-right: 10%;
}

ul{
    display: flex;
    list-style: none;
    gap: 15%;
    text-decoration: none;
}

a {
    text-decoration: none;
}

.botao{
    color: #d3d3d3;
}

.botao:hover{
    color: darkgrey;
}

</style>
