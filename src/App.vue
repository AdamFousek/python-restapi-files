<template>
    <div class="container">
        <div class="row">
            <div class="col-xs-12 text-center">
                <router-view></router-view>
            </div>
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
    created() {
        const instance = axios.create({ baseURL: this.$serverUrl });

        instance
            .get('/helloo')
            .then((response) => {
                console.log(response);
            })
            .catch((error) => {
                console.log(error);
            });
    },
};
</script>

<style>
body {
    background-color: #34495e;
    color: #bdc3c7;
}
</style>
