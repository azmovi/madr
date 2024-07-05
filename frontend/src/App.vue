<script setup>
import { RouterLink, RouterView } from 'vue-router';
import SiteNav from '@/components/SiteNav.vue'
</script>

<template>
    <header>
        <SiteNav />
    </header>
    <main>
        <RouterView />
    </main>
</template>

<style scoped>
</style>
