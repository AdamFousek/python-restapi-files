<template>
    <div>
        <h1>Set your default path and restrictions or go to directories</h1>

        <router-link to="/setting" class="btn btn-primary"
            >Settings</router-link
        >
        <router-link to="/directories" class="btn btn-primary"
            >Directories</router-link
        >
    </div>
</template>

<script>
export default {};
</script>

<style scoped>
h1 {
    padding: 30px 0;
}
.btn {
    margin: 30px;
}
</style>
