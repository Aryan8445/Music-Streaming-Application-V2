<template>
    <div>
        <h1>User Profile</h1>
        <div>
            <p>{{ user.name }}</p>
        </div>
        <div>
            <p>{{ user.email }}</p>
        </div>
    </div>
</template>

<script>
export default {
    /* eslint-disable*/
    name: "UserProfile",
    data() {
        return {
            user: {
                name: "Aryan",
                email: "aryan@example.com"
            }
        }
    }
}
</script>