<template>
    <div class="col-sm">
        <h2>Settings</h2>
        <div class="mt-2 mb-2">
            <a class="btn btn-warning" @click="loadDirectories">
                Load directories
            </a>
            <a class="btn btn-success" @click="editPaths = !editPaths">
                Edit paths
            </a>
        </div>
        <div v-if="editPaths" class="form-group change-dir">
            <small>One line one path!</small>
            <textarea
                v-model="userPaths"
                placeholder="Paths with comma separated"
                class="form-control"
            ></textarea>
            <button @click="updateDirectories()" class="btn btn-success">
                Update Paths
            </button>
        </div>
        <h4>Current allowed paths:</h4>
        <ul class="list-group">
            <li
                class="list-group-item"
                v-for="(path, index) in paths"
                :key="index"
            >
                {{ path }}
            </li>
        </ul>
        <div>
            <router-link to="/" class="btn btn-primary"
                >Back to homepage</router-link
            >
        </div>
    </div>
</template>

<script>
import axios from 'axios';
export default {
    data() {
        return {
            axiosInstance: axios.create({ baseURL: this.$serverUrl }),
            userPaths: '',
            editPaths: false,
            paths: [],
        };
    },
    methods: {
        loadDirectories() {
            this.axiosInstance
                .get('/settings')
                .then((response) => {
                    this.paths = response.data.data;
                    this.userPaths = response.data.data.join('\r\n');
                })
                .catch((error) => {
                    this.message = error.response.data.message;
                });
        },
        updateDirectories() {
            this.axiosInstance
                .post('/settings', {
                    paths: this.userPaths.split('\r\n'),
                })
                .then((response) => {
                    this.message = 'Paths were set!';
                    this.loadDirectories();
                })
                .catch((error) => {
                    this.message = error.response.data.message;
                });
        },
    },
};
</script>

<style scoped></style>
