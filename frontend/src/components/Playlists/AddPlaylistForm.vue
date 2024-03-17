<template>
    <div>
        <h1>Add Playlist</h1>
        <form @submit.prevent="addPlaylist">
            <label for="name">Name:</label>
            <input type="text" id="name" v-model="playlistName" required>
            <button type="submit">Add Playlist</button>
        </form>
    </div>
</template>

<script>
export default {
    data() {
        return {
            playlistName: ''
        };
    },
    methods: {
        addPlaylist() {
            // Add your logic here to handle the form submission
            // For example, you can make an API call to save the playlist
            // and then navigate to a different page
        }
    }
};
</script>

<style scoped>
/* Add your custom styles here */
</style>