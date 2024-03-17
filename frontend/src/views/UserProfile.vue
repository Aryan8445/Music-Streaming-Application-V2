<template>
    <div class="user-profile">
        <h1>{{ user.name }}</h1>
        <p>{{ user.email }}</p>
        <p>{{ user.bio }}</p>
        <img :src="user.avatar" alt="User Avatar" />
    </div>
</template>

<script>
export default {
    data() {
        return {
            user: {
                name: 'John Doe',
                email: 'johndoe@example.com',
                bio: 'I am a software developer.',
                avatar: 'https://example.com/avatar.jpg'
            }
        };
    }
};
</script>

<style scoped>
.user-profile {
    text-align: center;
}
</style>