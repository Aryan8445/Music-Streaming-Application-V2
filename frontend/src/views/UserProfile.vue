<template>
    <div>
        <UserProfile @userprofile="UserProfile"></UserProfile>
    </div>
</template>

<script>
/* eslint-disable */
import UserProfile from '@/components/Auth/UserProfile.vue';
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
    },
    components: {
          UserProfile  
    }
};
</script>

<style scoped>
.user-profile {
    text-align: center;
}
</style>