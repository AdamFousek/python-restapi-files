<template>
    <tr>
        <th>{{ dir.name }}</th>
        <td>{{ dir.created_at | readable }}</td>
        <td>{{ dir.last_modification_at | readable }}</td>
        <td>{{ dir.size | size }}</td>
        <td>{{ dir.is_file }}</td>
        <td>{{ dir.is_dir }}</td>
    </tr>
</template>

<script>
export default {
    props: ['dir'],
};
</script>

<style scoped></style>
