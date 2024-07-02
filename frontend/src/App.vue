<template>
    <div class="flex flex-col min-h-screen font-FiraCode bg-black-primary">
        <RouterView />
        <SiteNav />
    </div>
</template>

<script>
import { RouterView } from "vue-router";
import SiteNav from "./components/SiteNav.vue";
</script>
