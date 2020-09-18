<template>
    <div class="col-sm">
        <h2>Directory structure</h2>
        <small>Current path: {{ realPath }}</small>
        <div class="mt-2 mb-2">
            <a class="btn btn-warning" @click="changeDir = !changeDir"
                >Change directory</a
            >
            <a class="btn btn-success" @click="createDirC = !createDirC"
                >Create directory</a
            >
            <a class="btn btn-success" @click="createFileC = !createFileC"
                >Create file</a
            >
        </div>
        <div v-if="createDirC" class="form-group change-dir">
            <input class="form-control" type="text" v-model="dirName" />
            <button @click="createDir()" class="btn btn-success">
                Create Directory
            </button>
        </div>
        <div v-if="createFileC" class="form-group change-dir">
            <input class="form-control" type="text" v-model="fileName" />
            <button @click="createFile()" class="btn btn-success">
                Create File
            </button>
        </div>
        <div v-if="changeDir" class="form-group change-dir">
            <input class="form-control" type="text" v-model="path" />
            <button @click="changePath()" class="btn btn-warning">
                Change Path
            </button>
        </div>
        <div v-if="message != ''">
            <p><strong>{{ message }}</strong></p>
        </div>
        <div class="card w-50 mb-1 mt-1" v-if="file.show">
            <div class="card-body">
                <h5 class="card-title">{{ file.name }}</h5>
                <p class="card-text">
                    <p>Created at: {{ file.created_at | readable }}</p>
                    <p>Last modification at {{ file.last_modification_at | readable }}</p>
                    <p>Size: {{ file.size | size }}</p>
                    <p>Full path: {{ realPath }}{{ file.name }}</p>
                </p>
                <a @click="deleteFile(file)" class="btn btn-danger">Remove file</a>
            </div>
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
                    <th scope="col">Delete</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(dir, index) in dirs" :key="index" :dir="dir">
                    <th>
                        <a
                            @click="
                                dir.is_file ? changeFile(dir) : changePath(dir)
                            "
                            > {{ dir.name }} </a
                        >
                    </th>
                    <td>{{ dir.created_at | readable }}</td>
                    <td>{{ dir.last_modification_at | readable }}</td>
                    <td>{{ dir.size | size }}</td>
                    <td>{{ dir.is_file }}</td>
                    <td>{{ dir.is_dir }}</td>
                    <td> <a class="btn btn-danger" @click="deleteDir(dir)" v-if="dir.is_dir">Delete</a></td>
                </tr>
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
import axios from 'axios';

export default {
    data() {
        return {
            axiosInstance: axios.create({ baseURL: this.$serverUrl }),
            changeDir: false,
            createDirC: false,
            createFileC: false,
            path: '',
            realPath: '',
            message: '',
            dirs: [],
            fileName: '',
            dirName: '',
            file: {
                show: false,
            },
        };
    },
    methods: {
        changePath(dir) {
            this.file.show = false;
            let path = ""
            if (dir) {
                if (this.path.endsWith("/") || this.path.endsWith("\\")) {
                    path = this.path + dir.name;
                } else {
                    path = this.path + '/' + dir.name;
                }
                
            } else {
                path = this.path;
                this.changeDir = !this.changeDir;
            }
            this.axiosInstance
                .put('/directory', {
                    path: path,
                })
                .then((response) => {
                    this.message= '';
                    this.loadDir();
                    this.path = path
                    this.realPath = path;
                })
                .catch((error) => {
                    this.message = error.response.data.message;
                });
        },
        changeFile(dir) {
            this.axiosInstance
                .put('/file', {
                    file_name: dir.name,
                })
                .then((response) => {
                    this.message= '';
                    this.loadFile();
                })
                .catch((error) => {
                    this.message = error.response.data.message;
                });
        },
        loadDir() {
            this.axiosInstance
                .get('/directory')
                .then((response) => {
                    this.message= '';
                    this.dirs = response.data.data;
                })
                .catch((error) => {
                    this.message = error.response.data.message;
                });
        },
        loadFile() {
            this.axiosInstance
                .get('/file')
                .then((response) => {
                    this.message= '';
                    let file = response.data.data;
                    this.file.name = file.name;
                    this.file.created_at = file.created_at;
                    this.file.last_modification_at = file.last_modification_at;
                    this.file.size = file.size;
                    this.file.show = true;
                })
                .catch((error) => {
                    this.message = error.response.data.message;
                });
        },
        createDir() {
            this.axiosInstance
                .post('/directory', {
                    dir_name: this.dirName,
                })
                .then((response) => {
                    this.message = "Directory was created!";
                    this.loadDir();
                })
                .catch((error) => {
                    this.message = error.response.data.message;
                });
        },
        deleteDir(dir) {
            this.axiosInstance
                .delete('/directory', {
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    data: {
                        dir_name: dir.name,
                    }
                })
                .then((response) => {
                    this.message = "Directory was deleted!"
                    this.loadDir();
                })
                .catch((error) => {
                    this.message = error.response.message;
                });
        },
        createFile() {
            this.axiosInstance
                .post('/file', {
                    file_name: this.fileName,
                })
                .then((response) => {
                    this.message = "File was created!";
                    this.loadDir();
                })
                .catch((error) => {
                    this.message = error.response.data.message;
                });
        },
        deleteFile(file) {
            this.axiosInstance
                .delete('/file', {
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    data: {
                        file_name: file.name,
                    }
                })
                .then((response) => {
                    this.message = "File was deleted!"
                    this.loadDir();
                })
                .catch((error) => {
                    this.message = error.response.data.message;
                });
        }
    },
    create() {
        this.axiosInstance
            .get('/directory')
            .then((response) => {
                this.message= '';
                this.dirs = response.data.data;
            })
            .catch((error) => {
                this.message = error.response.data.message;
            });
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
