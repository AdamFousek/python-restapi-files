<template>
    <div class="container">
        <div class="row">
            <router-view></router-view>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
export default {
    data() {
        return {
            data: '',
        };
    },
};
</script>

<style>
body {
    background-color: #34495e;
    color: #bdc3c7;
}
</style>
