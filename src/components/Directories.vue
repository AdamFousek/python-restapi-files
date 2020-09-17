<template>
    <div>
        <h2>Directory structure</h2>
        <small>Current path: {{ path }}</small>
        <div>
            <a href="#" @click="changeDir = !changeDir">Change dir</a>
        </div>
        <div v-if="changeDir" class="form-group change-dir">
            <input class="form-control" type="text" v-model="route" />
            <button @click="changePath()" class="btn btn-warning">
                Submit
            </button>
        </div>

        <table class="table table-striped table-dark">
            <thead>
                <tr>
                    <th scope="col">Name</th>
                    <th scope="col">Created at</th>
                    <th scope="col">Last modification at</th>
                    <th scope="col">Size</th>
                    <th scope="col">File</th>
                    <th scope="col">Directory</th>
                </tr>
            </thead>
            <tbody>
                <app-dir
                    v-for="(dir, index) in dirs"
                    :key="index"
                    :dir="dir"
                ></app-dir>
            </tbody>
        </table>
        <div>
            <router-link to="/" class="btn btn-primary"
                >Back to homepage</router-link
            >
        </div>
    </div>
</template>

<script>
import DirectoryVue from './Directory.vue';
import axios from 'axios';

export default {
    data() {
        return {
            route: '',
            changeDir: false,
            path: '',
            dirs: [
                {
                    name: 'name',
                    created_at: 1592298290.7698877,
                    last_modification_at: 1592298377.1869373,
                    size: 273862,
                    is_file: true,
                    is_dir: false,
                },
            ],
        };
    },
    methods: {
        changePath() {
            this.path = this.route;
        },
    },
    components: {
        appDir: DirectoryVue,
    },
    watch: {
        path(val) {
            axios({
                method: 'get',
                url: this.$serverUrl + 'directory',
                params: {
                    path: val,
                },
            })
                .then((response) => {
                    console.log(response);
                })
                .catch((error) => {
                    console.log(error);
                });
        },
    },
};
</script>

<style scoped>
.change-dir {
    margin: 15px 0;
}
.change-dir input {
    margin: 10px 0;
}
</style>
